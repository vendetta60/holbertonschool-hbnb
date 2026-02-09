#!/usr/bin/python3
"""To add amenities"""

import uuid
from datetime import datetime

class Amenity:
    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self._validate()

    def _validate(self):
        if not self.name or len(self.name) > 50:
            raise ValueError("Name musst be 1-50 characters")

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key):
        self.save()
        self._validate()
