from flask import Blueprint, request, jsonify
from app.dao import player_dao
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.dao.player_dao import get_player_by_username, get_top_players_by_wins

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

@player_bp.route('/players/<string:username>/role', methods=['PUT'])
@jwt_required()
def update_player_role(username):
    requester_username = get_jwt_identity()
    requester = get_player_by_username(requester_username)

    if not requester or requester.player_role != "manager":
        return jsonify({"error": "فقط مدیرها می‌توانند نقش بازیکنان را تغییر دهند"}), 403

    data = request.get_json()
    new_role = data.get("player_role")

    if new_role not in ["admin", "manager", "normal"]:
        return jsonify({"error": "نقش وارد شده نامعتبر است. نقش باید 'admin' یا 'manager'یا 'normal' باشد"}), 400

    target_player = get_player_by_username(username)
    if not target_player:
        return jsonify({"error": "بازیکن مورد نظر پیدا نشد"}), 404

    success = player_dao.update_player_role(username, new_role)
    if not success:
        return jsonify({"error": "خطا در تغییر نقش بازیکن"}), 500

    # Persian response:
    return jsonify({"message": f"نقش بازیکن '{username}' با موفقیت به '{new_role}' تغییر یافت"}), 200

@player_bp.route("/players", methods=["GET"])
@jwt_required()
def get_player_username():
    username = get_jwt_identity()
    return jsonify({"username": username})


@player_bp.route("/players/top_winners", methods=["GET"])
@jwt_required()
def get_top_winners_route():
    top_players = get_top_players_by_wins(5)
    return jsonify(top_players)

@player_bp.route("/get_user", methods=["GET"])
@jwt_required()
def get_user_by_username_route():
    username = get_jwt_identity()
    player = player_dao.get_player_by_username(username)

    if not player:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "player_id": player.player_id,
        "username": player.username,
        "email": player.email,
        "signup_date": player.signup_date,
        "player_role": player.player_role,
    })