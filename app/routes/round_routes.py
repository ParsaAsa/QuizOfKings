from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from dao.round_dao import create_round, get_round, update_round_state

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
