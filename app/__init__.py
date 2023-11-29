from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from app.controllers.game import game
    from app.controllers.auth import auth

    app.register_blueprint(game, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from app.models.player import Player

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_player(id):
        return Player.query.get(int(id))

    # Custom 404 error handler
    @app.errorhandler(404)
    def not_found_error(error):
        return "<h1>404 Page not found</h1><p>The resource could not be found.</p>", 404

    return app


def create_database(app):
    with app.app_context():
        db.create_all()
        print("Created Database!")

if __name__ == "app":
    app = create_app()
    create_database(app)
    app.run(debug=True)
