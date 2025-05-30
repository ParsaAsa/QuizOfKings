from flask import Blueprint, request, jsonify
from app.dao import player_dao

player_bp = Blueprint('player', __name__)

@player_bp.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = player_dao.get_player_by_id(player_id)
    if player:
        return jsonify(player.__dict__)
    return jsonify({"error": "Player not found"}), 404

@player_bp.route('/players', methods=['POST'])
def register_player():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    player_password = data.get("player_password")
    player_role = data.get("player_role", "normal")

    if not all([username, email, player_password]):
        return jsonify({"error": "Missing fields"}), 400

    player_id = player_dao.create_player(username, email, player_password, player_role)
    return jsonify({"player_id": player_id}), 201
