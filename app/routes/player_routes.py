from flask import Blueprint, request, jsonify
from app.dao import player_dao
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.dao.player_dao import get_player_by_username

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

@player_bp.route('/players/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    player = get_player_by_username(username)

    if not player or player.player_password != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=player.username)
    return jsonify(access_token=access_token)
