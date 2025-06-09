from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dao import question_dao, player_dao
from app.entities.question import Question

question_bp = Blueprint("question_bp", __name__)

@question_bp.route("/questions", methods=["POST"])
@jwt_required()
def create_question_route():
    data = request.get_json()
    username = get_jwt_identity()
    player = player_dao.get_player_by_username(username)

    if not player or player.player_role not in ["normal", "admin", "manager"]:
        return jsonify({"error": "Unauthorized"}), 403

    # Build the Question object
    question = Question(
        question_id=0,  # Placeholder, will be filled in by DB
        question_text=data["question_text"],
        right_option=data["right_option"],
        difficulty=data["difficulty"],
        confirmed=None,  # Will be overridden by DAO based on role
        option_A=data["option_A"],
        option_B=data["option_B"],
        option_C=data["option_C"],
        option_D=data["option_D"],
        category_id=data["category_id"],
        author_id=player.player_id
    )

    created_question = question_dao.create_question(question, player.player_role)
    return jsonify(created_question.__dict__), 201

@question_bp.route("/questions/<int:question_id>", methods=["PUT"])
@jwt_required()
def update_question_route(question_id):
    username = get_jwt_identity()
    player = player_dao.get_player_by_username(username)

    if player.player_role not in ["admin", "manager"]:
        return jsonify({"error": "Only admin or manager can update questions"}), 403

    data = request.get_json()

    question = Question(
        question_id=question_id,
        question_text=data["question_text"],
        right_option=data["right_option"],
        difficulty=data["difficulty"],
        confirmed=None,  # This will be returned from DB, not passed in
        option_A=data["option_A"],
        option_B=data["option_B"],
        option_C=data["option_C"],
        option_D=data["option_D"],
        category_id=data["category_id"],
        author_id=player.player_id  # This will be ignored on update, but needed for entity
    )

    updated_question = question_dao.update_question(question)

    if updated_question:
        return jsonify(updated_question.__dict__)
    return jsonify({"error": "Question not found or update failed"}), 404

@question_bp.route("/questions/<int:question_id>", methods=["DELETE"])
@jwt_required()
def delete_question_route(question_id):
    username = get_jwt_identity()
    player = player_dao.get_player_by_username(username)

    if not player:
        return jsonify({"error": "Unauthorized"}), 403

    success = question_dao.delete_question(question_id, player)
    if success:
        return jsonify({"message": "Question deleted"})
    return jsonify({"error": "Question not found or delete not allowed"}), 404

@question_bp.route("/questions/<int:question_id>/accept", methods=["POST"])
@jwt_required()
def accept_question_route(question_id):
    data = request.get_json()
    confirmed = data.get("confirmed")

    if confirmed not in [True, False]:
        return jsonify({"error": "Confirmed must be true or false"}), 400

    username = get_jwt_identity()
    player = player_dao.get_player_by_username(username)

    if player.player_role not in ["admin", "manager"]:
        return jsonify({"error": "Only admin or manager can accept questions"}), 403

    question = question_dao.get_question_by_id(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    if question.author_id == player.player_id:
        return jsonify({"error": "You cannot accept your own question"}), 400

    success = question_dao.accept_question(question_id, player.player_id, confirmed)
    if success:
        return jsonify({"message": "Question confirmation status updated"})
    return jsonify({"error": "Failed to update confirmation"}), 500

@question_bp.route("/questions/unconfirmed", methods=["GET"])
@jwt_required()
def get_unconfirmed_questions_route():
    username = get_jwt_identity()
    player = player_dao.get_player_by_username(username)

    if not player or player.player_role not in ["admin", "manager"]:
        return jsonify({"error": "Only admin or manager can view unconfirmed questions"}), 403

    questions = question_dao.get_unconfirmed_questions()
    return jsonify(questions)