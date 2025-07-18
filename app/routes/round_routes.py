from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dao.round_dao import create_round, get_round, update_round_state, set_round_category
from app.dao.player_answer_dao import initial_questions
from app.dao.player_dao import get_player_by_username
from app.dao.match_dao import get_match_by_id

round_bp = Blueprint('round_bp', __name__)

@round_bp.route("/rounds", methods=["POST"])
@jwt_required()
def create_round_route():
    data = request.get_json()
    match_id = data.get("match_id")
    round_number = data.get("round_number")

    if not match_id or not round_number:
        return jsonify({"error": "match_id and round_number required"}), 400

    try:
        round_obj = create_round(match_id, round_number)
        return jsonify(round_obj.__dict__), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@round_bp.route("/rounds/<int:match_id>/<int:round_number>", methods=["GET"])
@jwt_required()
def get_round_route(match_id, round_number):
    round_obj = get_round(match_id, round_number)
    if not round_obj:
        return jsonify({"error": "Round not found"}), 404
    return jsonify(round_obj.__dict__)

@round_bp.route("/rounds/<int:match_id>/<int:round_number>/state", methods=["PUT"])
@jwt_required()
def update_round_state_route(match_id, round_number):
    data = request.get_json()
    new_state = data.get("round_state")

    if new_state not in ['not_started', 'player1_turn', 'player2_turn', 'done']:
        return jsonify({"error": "Invalid round_state"}), 400

    round_obj = update_round_state(match_id, round_number, new_state)
    if not round_obj:
        return jsonify({"error": "Round not found or update failed"}), 404

    return jsonify(round_obj.__dict__)

@round_bp.route("/rounds/<int:match_id>/<int:round_number>/category", methods=["PUT"])
@jwt_required()
def set_round_category_route(match_id, round_number):
    data = request.get_json()
    category_id = data.get("category_id")

    if category_id is None:
        return jsonify({"error": "category_id is required"}), 400

    username = get_jwt_identity()
    player = get_player_by_username(username)
    if not player:
        return jsonify({"error": "Unauthorized"}), 403

    match = get_match_by_id(match_id)
    if not match:
        return jsonify({"error": "Match not found"}), 404

    round_obj = get_round(match_id, round_number)
    if not round_obj:
        return jsonify({"error": "Round not found"}), 404

    # Block if round_state is 'not_started'
    if round_obj.round_state == "not_started":
        return jsonify({"error": "Cannot set category before round starts"}), 400

    # Determine who should set the category based on round_number
    if round_number % 2 == 0:
        allowed_player_id = match.player1_id
    else:
        allowed_player_id = match.player2_id

    if player.player_id != allowed_player_id:
        return jsonify({"error": "You are not allowed to set category for this round"}), 403

    try:
        round_obj = set_round_category(match_id, round_number, category_id)
        if not round_obj:
            return jsonify({"error": "Round not found or category update failed"}), 404

        initial_questions(match_id, round_number)
        return jsonify(round_obj.__dict__)
    except Exception as e:
        return jsonify({"error": str(e)}), 500