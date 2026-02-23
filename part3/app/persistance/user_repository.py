from app.models.user import User
from app import db
from app.persistance.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
    
    def is_email_registered(self, email):
        return self.model.query.filter_by(email=email).count() > 0
    
    def get_admin_users(self):
        return self.model.query.filter_by(is_admin=True).all()