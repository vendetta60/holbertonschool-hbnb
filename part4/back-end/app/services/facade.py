"""This class handles communication within the 3 arquitecture layers"""
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistance.repository import SQLAlchemyRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_place(self, place_data):
        title = place_data.get("title")
        price = place_data.get("price")
        latitude = place_data.get("latitude")
        longitude = place_data.get("longitude")

        if not title:
            raise ValueError("Title is required")
        if price < 0 or not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise ValueError("Invalid price, latitude or longitude")

        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            place_data.get('title'),
            place_data.get('description'),
            place_data.get('price'),
            place_data.get('latitude'),
            place_data.get('longitude'),
            owner
        )

        amenity_ids = place_data.get('amenities', []) or []
        for amen_id in amenity_ids:
            amenity = self.amenity_repo.get(amen_id)
            if amenity:
                place.add_amenity(amenity)
        self.place_repo.add(place)
        return place

    def get_all_places(self):
        """Get all places from the repository"""
        return self.place_repo.get_all()

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place

    def get_place_details(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner = self.user_repo.get(place.owner.id)
        amenities = [self.amenity_repo.get(amenity_id) for amenity_id in place.amenities]
        reviews = self.review_repo.get_reviews_by_place(place.id)

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email
            } if owner else None,
            "amenities": [
                {"id": amenity.id, "name": amenity.name}
                for amenity in amenities if amenity
            ],
            "reviews": [
                {
                    "id": review.id,
                    "text": review.text,
                    "rating": review.rating,
                    "user_id": review.user.id
                } for review in reviews
            ]
        }


    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return "not_found"

        try:
            place.update(place_data)
            return place
        except ValueError:
            return "invalid_data"

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, update_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        try:
            amenity.update(update_data)
            self.amenity_repo.update(amenity_id, update_data)
            return amenity
        except ValueError as e:
            return str(e)

    def create_user(self, user_data):
        plaintext_pw = user_data.get('password')
        data = {k: v for k, v in user_data.items() if k != 'password'}
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        original_email = user.email

        user.update(update_data)

        if 'email' in update_data and update_data['email'] != original_email:
            existing_user = self.get_user_by_email(update_data['email'])
            if existing_user and existing_user.id != user_id:
                return 'email_exists'

        self.user_repo.update(user_id, update_data)
        return user

    def create_review(self, review_data):
        text = review_data.get('text')
        rating = review_data.get('rating', 1)
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        if rating < 1 or rating > 5:
            raise ValueError("Invalid rating")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        review = Review(text, rating, place, user)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]
    
    def get_user_review_for_place(self, user_id, place_id):
        for rev in self.review_repo.get_all():
            if rev.user.id == user_id and rev.place.id == place_id:
                return rev
        return None

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        review.update(review_data)
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        self.review_repo.delete(review_id)
        return True