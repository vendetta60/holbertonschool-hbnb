#!/usr/bin/python3
"""Creates user"""

import re
import uuid
from datetime import datetime

class User:
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.email = kwargs.get('email', '')
        self.is_admin = kwargs.get('is_admin', False)

    def _validate(self):
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError("First name must be 1-50 characters")

        if not self.last_name or len(self.last_name) > 50:
            raise ValueError("Last name must be 1-50 characters")

        if not self.email or not self.EMAIL_REGEX.match(self.email):
            raise ValueError("Invalid email format")

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
