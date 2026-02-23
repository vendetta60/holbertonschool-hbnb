from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

ns = Namespace('places', description='Place operations')


amenity_model = ns.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = ns.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = ns.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating (1-5'),
    'user_id': fields.String(description='User ID')
})

place_model = ns.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, description="List of amenity IDs"),
})

@ns.route('/')
class PlaceList(Resource):
    @jwt_required()
    @ns.expect(place_model)
    @ns.response(201, 'Place successfully created')
    @ns.response(400, 'Invalid input data')
    def post(self):
        current_user = get_jwt_identity()
        data = ns.payload
        
        required_fields = ['title', 'price', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return {'error': f"'{field}' is a required property"}, 400
        
        data['owner_id'] = current_user
        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @ns.response(200, 'List of places retrieved successfully')
    def get(self):
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

    @jwt_required()
    @ns.response(403, 'Unauthorized action')
    def put(self):
        return {'error': 'Unauthorized action'}, 403

@ns.route('/<string:place_id>')
class PlaceResource(Resource):
    @ns.response(200, 'Place details retrieved successfully')
    @ns.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place_details(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place, 200

    @jwt_required()
    @ns.expect(place_model)
    @ns.response(200, 'Place updated successfully')
    @ns.response(404, 'Place not found')
    @ns.response(400, 'Invalid input data')
    def put(self, place_id):
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        data = ns.payload
        existing = facade.get_place(place_id)
        if not existing:
            return {'error': 'Place not found'}, 404
            
        if not is_admin and existing.owner.id != current_user:
            return {'error': 'Unauthorized action'}, 403
            
        updated = facade.update_place(place_id, data)
        if updated == 'invalid_data':
            return {'error': 'Invalid input data'}, 400
        return updated.to_dict(), 200
