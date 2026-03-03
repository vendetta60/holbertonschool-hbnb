"""Creates user"""
import re
import uuid
from app.models.baseclass import BaseModel
from datetime import datetime
from app.extensions import bcrypt
from app import db

class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', back_populates='user', lazy=True)

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.email = kwargs.get('email', '')
        raw_pw = kwargs.get('password', '')
        self.password = ''
        if raw_pw:
            self.hash_password(raw_pw)
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
            if hasattr(self, key):
                if key == 'password' and value:
                    self.hash_password(value)
                else:
                    setattr(self, key, value)
        self.save()

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, raw_password: str) -> bool:
        if not self.password or not raw_password:
            return False
        try:
            return bcrypt.check_password_hash(self.password, raw_password)
        except ValueError:
            return False