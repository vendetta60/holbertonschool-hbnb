from flask import Flask, Blueprint
from flask_restx import Api
from app.api.v1 import register_namespaces

def create_app():
    app = Flask(__name__)

    blueprint = Blueprint('api', __name__)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='__init__: HBnB Accommodation Service API',
        )

    register_namespaces(api)

    return app
