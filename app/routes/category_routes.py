from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dao.player_dao import get_player_by_username
from app.dao.category_dao import create_category, get_category_by_title

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category_route():
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    username = get_jwt_identity()
    player = get_player_by_username(username)

    if player is None or player.player_role not in ["admin", "manager"]:
        return jsonify({"error": "Unauthorized"}), 403

    category = create_category(title)
    return jsonify({"category_id": category.category_id, "title": category.title}), 201

@category_bp.route('/categories/<string:title>', methods=['GET'])
@jwt_required()
def get_category_route(title):
    category = get_category_by_title(title)
    if category is None:
        return jsonify({"error": "Category not found"}), 404

    return jsonify({"category_id": category.category_id, "title": category.title}), 200
