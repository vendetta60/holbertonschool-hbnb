#!/usr/bin/python3
"""Allows to write review"""
from app.models.baseclass import BaseModel
from app import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    user = db.relationship('User', back_populates='reviews', lazy=True)

    def __init__(self, text: str, rating: int):
        self.text = text
        self.rating = rating

    def _validate(self):
        if not self.text:
            raise ValueError("Review text is required")

        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating
        }