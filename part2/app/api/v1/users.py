from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade
from app.models.user import User

ns = Namespace('users', description='User operations')

facade = HBnBFacade()

user_model = ns.model('User', {
    'first_name': fields.String(
        required=True,
        description='First name of the user',
        max_lenght=50
    ),
    'last_name': fields.String(
        required=True,
        description='Last name of the user',
        max_lenght=50
    ),
    'email': fields.String(
        required=True,
        description='Email address of the user',
        pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$'
    ),
    'is_admin': fields.String(
        description='Admin privileges status',
        default=False
    )
})

user_response = ns.model('User_Response', {
    'id': fields.String(description='Unique user ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Admin status')
})

@ns.route('/')
class UserList(Resource):
    @ns.expect(user_model, validate=True)
    @ns.response(201, 'User created successfully', user_response)
    @ns.response(400, 'Validate error')
    def post(self):
        user_data = ns.payload

        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin': new_user.is_admin
                }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @ns.response(200, 'User list retrieved', [user_response])
    def get(self):
        users = facade.user_repo.get_all()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        } for user in users], 200

@ns.route('/<string:user_id>')
class UserResource(Resource):
    @ns.response(200, 'User details retrieved', user_response)
    @ns.response(404, 'User not found')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

    @ns.expect(user_model, validate=False)
    @ns.response(200, 'User updated successfully', user_response)
    @ns.response(400, 'Validation error')
    @ns.response(404, 'User not found')
    def put(self, user_id):
        user = facade.user_repo.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        update_data = ns.payload

        if 'email' in update_data and update_data['email'] != user.email:
            existing_user = facade.user_repo.get_by_attribute('email', update_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

        try:
            for key, value in update_data.items():
                setattr(user, key, value)

            facade.user_repo.update(user_id, update_data)

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': update_user.last_name,
                'email': update_user.email,
                'is_admin': updated_user.is_admin
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
