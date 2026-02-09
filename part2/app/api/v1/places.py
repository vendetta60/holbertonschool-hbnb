from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade

ns = Namespace('places', description='Place operations')

facade = HBnBFacade()

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
    'title': fields.String(required=True, description='Ttile of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model))
})

class PlaceList(Resource):
    @ns.expect(place_model)
    @ns.response(201, 'Place successfully created')
    @ns.response(400, 'Invalid input data')
    def post(self):
        data = ns.payload
        try:
            new_place = facade.create_place(data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @ns.response(200, 'List of places retrieved successfully')
    def get(self):
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

@ns.route('/<string:place_id>')
class PlaceResource(Resource):
    @ns.response(200, 'Place details retrieved successfully')
    @ns.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(full=True), 200

    @ns.expect(place_model)
    @ns.response(200, 'Place updated successfully')
    @ns.response(404, 'Place not found')
    @ns.response(400, 'Invalid input data')
    def put(self, place_id):
        data = ns.payload
        updated_place = facade.update_place(place_id, data)
        if updated_place == 'not found':
            return {'error': 'Place not found'}, 404
        elif updated_place == 'invalid_data':
            return {'error': 'Invalid input data'}, 400
        return {'message': 'Place updated successfully'}, 200
