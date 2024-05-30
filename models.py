from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for ORM
from flask import Flask

# Initialize SQLAlchemy
db = SQLAlchemy()

# User model for storing user data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user table
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username, must be unique and not null
    password = db.Column(db.String(120), nullable=False)  # Password, stored as a hashed string, not null
    favorites = db.relationship('Book', backref='user', lazy=True)  # Relationship to the Book model

# Book model for storing book data
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the book table
    title = db.Column(db.String(120), nullable=False)  # Title of the book, not null
    author = db.Column(db.String(120), nullable=False)  # Author of the book, not null
    genre = db.Column(db.String(120), nullable=False)  # Genre of the book, not null
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Foreign key to the user table, nullable
