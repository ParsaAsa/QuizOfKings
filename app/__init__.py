from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.routes.player_routes import player_bp
import os
from dotenv import load_dotenv
from app.routes.match_routes import match_bp
from app.routes.category_routes import category_bp
from app.routes.round_routes import round_bp

load_dotenv()  # Load from .env

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Set secret key for JWT
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") or "super-secret-key"

    # Initialize JWT
    JWTManager(app)

    # Register blueprints
    app.register_blueprint(player_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(round_bp)
    app.register_blueprint(category_bp)

    return app
