#!/usr/bin/python3
"""To add amenities"""
from app.models.baseclass import BaseModel
from app import db
from datetime import datetime

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    places = db.relationship('Place', secondary='place_amenity', back_populates='amenities')

    def __init__(self, name: str):
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self._validate()

    def _validate(self):
        if not self.name or len(self.name) > 50:
            raise ValueError("Name must be 1-50 characters")

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
        self._validate()