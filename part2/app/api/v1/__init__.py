"""__init__ initializes the v1 API package"""
from .users import ns as users_ns
from .places import ns as places_ns
from .reviews import ns as reviews_ns
from .amenities import ns as amenities_ns

def register_namespaces(api):
    api.add_namespace(users.ns, path='/api/v1/users')
    api.add_namespace(places.ns, path='/api/v1/places')
    api.add_namespace(reviews.ns, path='/api/v1/reviews')
    api.add_namespace(amenities.ns, path='/api/v1/amenities')
