from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dao.player_stat_dao import get_player_stat_by_username

player_stat_bp = Blueprint("player_stat", __name__)

@player_stat_bp.route("/player_stats/me", methods=["GET"])
@jwt_required()
def get_my_stats():
    username = get_jwt_identity()
    stat = get_player_stat_by_username(username)
    if not stat:
        return jsonify({"error": "Player not found or has no stats yet."}), 404

    return jsonify({
        "player_id": stat.player_id,
        "total_matches": stat.total_matches,
        "wins": stat.wins,
        "accuracy": round(stat.accuracy, 4)
    })

@player_stat_bp.route("/player_stats/<username>", methods=["GET"])
@jwt_required()
def get_player_stat_route(username):
    player_stat = get_player_stat_by_username(username)
    if not player_stat:
        return jsonify({"error": "Player not found"}), 404

    return jsonify({
        "player_id": player_stat.player_id,
        "total_matches": player_stat.total_matches,
        "wins": player_stat.wins,
        "accuracy": player_stat.accuracy
    })
