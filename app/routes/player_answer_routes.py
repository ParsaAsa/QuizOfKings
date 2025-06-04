from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dao.player_answer_dao import submit_answer_if_null, get_player_answers
from app.dao.match_dao import get_match_by_id, update_match_state
from app.dao.round_dao import get_round
from app.dao.player_answer_dao import get_player_by_username
from app.dao.round_dao import update_round_state

player_answer_bp = Blueprint("player_answer_bp", __name__)

@player_answer_bp.route("/player_answers/submit", methods=["POST"])
@jwt_required()
def submit_answer_route():
    data = request.get_json()
    match_id = data.get("match_id")
    round_number = data.get("round_number")
    question_number = data.get("question_number")
    answer = data.get("answer")
    username = get_jwt_identity()

    if not all([match_id, round_number, question_number, answer]):
        return jsonify({"error": "Missing required fields"}), 400

    match = get_match_by_id(match_id)
    if not match:
        return jsonify({"error": "Match not found"}), 404

    round_obj = get_round(match_id, round_number)
    if not round_obj:
        return jsonify({"error": "Round not found"}), 404

    player = get_player_by_username(username)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    # Check whose turn it is based on round state
    if round_obj.round_state == 'player1_turn' and player.player_id != match.player1_id:
        return jsonify({"error": "It's not your turn"}), 403
    elif round_obj.round_state == 'player2_turn' and player.player_id != match.player2_id:
        return jsonify({"error": "It's not your turn"}), 403
    elif round_obj.round_state not in ['player1_turn', 'player2_turn']:
        return jsonify({"error": "Round is not active"}), 400

    try:
        success = submit_answer_if_null(match_id, round_number, question_number, answer, player.player_id)
        if not success:
            return jsonify({"error": "Failed to submit answer (record may not exist)"}), 400

        # Check if player has now submitted all 3 answers
        answers = get_player_answers(match_id, round_number, player.player_id)
        answered_count = sum(1 for a in answers if a.player_answer is not None)

        if answered_count == 3:
            is_odd_round = round_number % 2 == 1
            round_done = False

            if is_odd_round:
                # Player2 starts, then player1
                if player.player_id == match.player2_id:
                    # Player2 finished → switch to player1
                    update_round_state(match_id, round_number, "player1_turn")
                elif player.player_id == match.player1_id:
                    # Player1 finished → round done
                    update_round_state(match_id, round_number, "done")
                    round_done = True
            else:
                # Player1 starts, then player2
                if player.player_id == match.player1_id:
                    # Player1 finished → switch to player2
                    update_round_state(match_id, round_number, "player2_turn")
                elif player.player_id == match.player2_id:
                    # Player2 finished → round done
                    update_round_state(match_id, round_number, "done")
                    round_done = True

            if round_done:
                if round_number == 6:
                    update_match_state(match_id, "done")
                else:
                    next_round = get_round(match_id, round_number + 1)
                    if next_round:
                        # Determine who starts next round
                        if (round_number + 1) % 2 == 0:
                            update_round_state(match_id, round_number + 1, "player1_turn")
                        else:
                            update_round_state(match_id, round_number + 1, "player2_turn")
                    else:
                        update_match_state(match_id, "done")

        return jsonify({"message": "Answer submitted successfully"})

    except (ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
