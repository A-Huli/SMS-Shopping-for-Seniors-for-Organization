from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from zakupy_dla_seniora.config import Config


db = SQLAlchemy()
login_manager = LoginManager()


def register_blueprints(app):
    from zakupy_dla_seniora.main.routes import main
    app.register_blueprint(main)

    from zakupy_dla_seniora.auth.routes import auth
    app.register_blueprint(auth)

    from zakupy_dla_seniora.volunteers.routes import volunteers
    app.register_blueprint(volunteers)

    from zakupy_dla_seniora.board.routes import board
    app.register_blueprint(board)

    from zakupy_dla_seniora.landing.routes import landing
    app.register_blueprint(landing)

def register_api_resources(api):
    pass


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)

    register_blueprints(app)
    # register_api_resources(api)

    db.init_app(app)
    login_manager.init_app(app)

    return app
