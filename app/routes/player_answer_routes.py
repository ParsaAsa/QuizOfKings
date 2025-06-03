from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dao.player_answer_dao import submit_answer_if_null

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

    try:
        success = submit_answer_if_null(match_id, round_number, question_number, answer, username)
        if success:
            return jsonify({"message": "Answer submitted successfully"}), 200
        else:
            return jsonify({"error": "Answer already submitted"}), 400
    except (ValueError, PermissionError) as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        import traceback
        traceback.print_exc()  # Log to console
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
