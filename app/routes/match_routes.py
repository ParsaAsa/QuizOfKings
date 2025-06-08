from flask import Blueprint, request, jsonify
from app.dao import match_dao
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dao.match_dao import accept_match_request, get_done_matches_by_username, get_match_requests_by_username, get_ongoing_matches_by_username
from app.dao.player_dao import get_player_by_username

match_bp = Blueprint('match_bp', __name__)

@match_bp.route('/matches/request', methods=['POST'])
@jwt_required()
def request_match():
    data = request.get_json()
    player2_username = data.get('player2_username')
    player1_username = get_jwt_identity()

    if not player2_username:
        return jsonify({"error": "Missing player2_username"}), 400

    if player1_username == player2_username:
        return jsonify({"error": "Cannot request a match with yourself"}), 400

    try:
        match_id = match_dao.create_match_request(player1_username, player2_username)
        return jsonify({"message": "Match request sent", "match_id": match_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@match_bp.route("/matches/accept", methods=["POST"])
@jwt_required()
def accept_match():
    data = request.get_json()

    match_id = data.get("match_id")
    accept = data.get("accept")  # must be boolean true/false

    if match_id is None:
        return jsonify({"error": "match_id is required"}), 400

    if accept is None or not isinstance(accept, bool):
        return jsonify({"error": "accept (boolean true or false) is required"}), 400

    player2_username = get_jwt_identity()

    success, msg = accept_match_request(match_id, player2_username, accept)
    if not success:
        return jsonify({"error": msg}), 400

    return jsonify({"message": msg}), 200

@match_bp.route("/matches/done", methods=["GET"])
@jwt_required()
def get_done_matches_route():
    username = get_jwt_identity()
    matches = get_done_matches_by_username(username)
    return jsonify(matches), 200


@match_bp.route("/matches/ongoing", methods=["GET"])
@jwt_required()
def get_ongoing_matches_route():
    username = get_jwt_identity()
    matches = get_ongoing_matches_by_username(username)
    return jsonify(matches), 200



@match_bp.route("/matches/pending_requests", methods=["GET"])
@jwt_required()
def get_pending_match_requests_route():
    username = get_jwt_identity()
    matches = get_match_requests_by_username(username)
    return jsonify(matches), 200
