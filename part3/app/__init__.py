from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from app.extensions import bcrypt, jwt

db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['JWT_SECRET_KEY'] = 'hbnb-project-pt3'

    db.init_app(app)

    from app.api.v1 import api_v1


    bcrypt.init_app(app)
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return {'error': 'Unauthorized action'}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return {'error': 'Unauthorized action'}, 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Unauthorized action'}, 401

    app.register_blueprint(api_v1)

    from flask import redirect
    @app.route('/')
    def index():
        return redirect('/api/v1/')

    return app
