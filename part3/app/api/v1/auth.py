from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.persistance.user_repository import UserRepository
from app.services import facade

ns = Namespace('auth', description='Authentication operations')

user_repo = UserRepository()

def check_admin_privileges():
    try:
        claims = get_jwt()
        return claims.get('is_admin', False)
    except:
        return False

def require_admin():
    if not check_admin_privileges():
        return {'error': 'Admin privileges required'}, 403
    return None

login_model = ns.model('Login',{
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        credentials = ns.payload
        user = facade.get_user_by_email(credentials['email'])

        print('Stored hash:', user.password if user else None,
              'Attempt:', credentials.get('password'))
        if not user:
            return {'error': 'Invalid credentials'}, 401
        if not user or not user.verify_password(credentials['password']):
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={'is_admin': user.is_admin}
            )
            return {'access_token': access_token}, 200
        if not user.verify_password(credentials.get('password')):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': user.is_admin}
        )
        return {'access_token': access_token}, 200