# app/__init__.py

from flask import Flask
from flask_cors import CORS
from app.routes.player_routes import player_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register all blueprints here
    app.register_blueprint(player_bp)

    return app
