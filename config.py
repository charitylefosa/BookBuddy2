import os

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-not-guess'
    
    # Database URI for SQLAlchemy to connect to the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///bookbuddy.db'
    
    # Disable SQLAlchemy's modification tracking feature - save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for JWT(Json Web Token) authentication
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'
