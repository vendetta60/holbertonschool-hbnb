"""__init__ initializes the v1 API package"""
from .auth import ns as auth_ns
from .users import ns as users_ns
from .places import ns as places_ns
from .reviews import ns as reviews_ns
from .amenities import ns as amenities_ns
from flask_restx import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(api_v1, version='1.0', title="HBnB API", doc='/')

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(amenities_ns, path='/amenities')

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        return {'message': f'Hello, user {user_id}'}, 200