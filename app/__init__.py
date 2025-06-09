from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from app.routes.player_routes import player_bp
from app.routes.match_routes import match_bp
from app.routes.category_routes import category_bp
from app.routes.round_routes import round_bp
from app.routes.question_routes import question_bp
from app.routes.player_answer_routes import player_answer_bp
from app.routes.player_stat_routes import player_stat_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Set secret key for JWT
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") or "super-secret-key"

    # Initialize JWT
    JWTManager(app)

    # Apply CORS to all /api/* routes, allow only localhost:3000
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    # Register all blueprints with url_prefix="/api"
    app.register_blueprint(player_bp, url_prefix="/api")
    app.register_blueprint(match_bp, url_prefix="/api")
    app.register_blueprint(round_bp, url_prefix="/api")
    app.register_blueprint(category_bp, url_prefix="/api")
    app.register_blueprint(question_bp, url_prefix="/api")
    app.register_blueprint(player_answer_bp, url_prefix="/api")
    app.register_blueprint(player_stat_bp, url_prefix="/api")

    @app.after_request
    def after_request(response):
        # Add CORS headers explicitly
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response

    return app
