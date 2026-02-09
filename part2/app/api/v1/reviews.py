from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import abort, jsonify

ns = Namespace('Review', description='Review related operations')

review_model = ns.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})

simple_review_model = ns.model('SimpleReview', {
    'id': fields.String,
    'text': fields.String,
    'rating': fields.Integer
})

@ns.route('/')
class ReviewList(Resource):
    @ns.expect(review_model)
    @ns.response(201, 'Review created')
    @ns.response(400, 'Invalid input')
    def post(self):
        data = ns.payload
        try:
            review = facade.create_review(data)
            return vars(review), 201
        except ValueError as e:
            return {"error": str(e)}, 400

@ns.route('/<review_id>')
class ReviewResource(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return vars(review), 200

    @ns.expect(review_model)
    @ns.response(200, 'Updated')
    @ns.response(404, 'Not found')
    @ns.response(400, 'Invalid data')
    def put(self, review_id):
        data = ns.payload
        updated = facade.updated_review(review_id, data)
        if not updated:
            return {"error": "Review not found"}, 404
        return {"message": "Review updated successfully"}

    @ns.response(200, 'Deleted')
    @ns.response(404, 'Not found')
    @ns.response(500, 'Server error')
    def delete(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            abort(404, 'Review not found')

        success = facade.delete_review(review_id)
        if not success:
            abort(500, 'Could not delete review')
        return {}, 200