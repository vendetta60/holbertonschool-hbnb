from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

ns = Namespace('users', description='User operations')
admin_ns = Namespace('admin', description='Admin operations')


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
    'password': fields.String(
        required=False,
        description='User password',
        min_length=6
    ),
    'is_admin': fields.Boolean(
        description='Admin privileges status',
        default=False
    )
})

user_update_model = ns.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address (admin only)'),
    'password': fields.String(description='Password (admin only)'),
    'is_admin': fields.Boolean(description='Admin status')
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
    @ns.response(403, 'Admin privileges required')
    def post(self):
        all_users = facade.user_repo.get_all()
        if len(all_users) == 0:
            is_admin_creator = True
        else:
            try:
                current_user = get_jwt_identity()
                claims = get_jwt()
                is_admin_creator = claims.get('is_admin', False)
                if not is_admin_creator:
                    return {'error': 'Admin privileges required'}, 403
            except:
                return {'error': 'Admin privileges required'}, 403

        user_data = ns.payload
        if is_admin_creator:
            user_data['is_admin'] = True

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
    @ns.marshal_list_with(user_response)
    def get(self):
        users = facade.user_repo.get_all()
        return users, 200

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

    @jwt_required()
    @ns.expect(user_update_model, validate=True)
    @ns.response(200, 'User updated successfully', user_response)
    @ns.response(400, 'Validation error')
    @ns.response(403, 'Unauthorized action')
    @ns.response(404, 'User not found')
    def put(self, user_id):
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin and current_user != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        update_data = ns.payload
        
        if not is_admin and ('email' in update_data or 'password' in update_data):
            return {'error': 'You cannot modify email or password'}, 400
        
        if is_admin and 'email' in update_data:
            existing_user = facade.get_user_by_email(update_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}, 400
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
            
        result = facade.update_user(user_id, update_data)
        if result is None:
            return {'error': 'User not found'}, 404
        if result == 'email_exists':
            return {'error': 'Email already registered'}, 400
            
        updated_user = result
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'is_admin': updated_user.is_admin
        }, 200

@admin_ns.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    @admin_ns.response(200, 'User updated successfully')
    @admin_ns.response(403, 'Admin privileges required')
    @admin_ns.response(404, 'User not found')
    @admin_ns.response(400, 'Email already in use')
    def put(self, user_id):
        """Admin endpoint for updating user details"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        data = request.json
        email = data.get('email')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            if updated_user is None:
                return {'error': 'User not found'}, 404
            if updated_user == 'email_exists':
                return {'error': 'Email already registered'}, 400
            
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin
            }, 200
        except Exception as e:
            return {'error': str(e)}, 400