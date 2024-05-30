import os

class Config:
    # Secret key for session management and other security-related features
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Database URI for SQLAlchemy to connect to the database
    # Uses an environment variable if available, otherwise defaults to a SQLite database file
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///bookbuddy.db'
    
    # Disable SQLAlchemy's modification tracking feature to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
<<<<<<< HEAD
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'

=======
    
    # Secret key for JWT authentication
    # Uses an environment variable if available, else defaults to a hardcoded secret
    # Change this in production to a secure random key
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'
>>>>>>> 9381b34025beebf4c5d19858c3b35927545cffdf
