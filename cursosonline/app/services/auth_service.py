from flask_bcrypt import Bcrypt
from app.models import User, db
import jwt
from datetime import datetime, timedelta
from flask import current_app

class AuthService:
    bcrypt = Bcrypt()
    
    @classmethod
    def hash_password(cls, password):
        """
        Hash a password
        
        :param password: Plain text password
        :return: Hashed password
        """
        return cls.bcrypt.generate_password_hash(password).decode('utf-8')
    
    @classmethod
    def check_password(cls, hashed_password, plain_password):
        """
        Check if the provided password matches the hashed password
        
        :param hashed_password: Stored hashed password
        :param plain_password: Plain text password to check
        :return: Boolean indicating password match
        """
        return cls.bcrypt.check_password_hash(hashed_password, plain_password)
    
    @classmethod
    def create_superadmin(cls):
        """
        Create a superadmin user if not exists
        """
        existing_admin = User.query.filter_by(role='admin', username='superadmin').first()
        if not existing_admin:
            superadmin = User(
                username='superadmin',
                email='superadmin@coursesplatform.com',
                password=cls.hash_password('SuperAdmin2023!'),
                role='admin'
            )
            db.session.add(superadmin)
            db.session.commit()
    
    @classmethod
    def generate_token(cls, user):
        """
        Generate JWT token for user authentication
        
        :param user: User object
        :return: JWT token
        """
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @classmethod
    def decode_token(cls, token):
        """
        Decode and validate JWT token
        
        :param token: JWT token
        :return: Decoded payload
        """
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None