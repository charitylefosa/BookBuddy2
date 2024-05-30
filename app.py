from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    print("Home route accessed")
    return jsonify(message="Welcome to BookBuddy!")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(f"Registering user: {data}")
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered successfully!")

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(f"Login attempt: {data}")
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token)
    else:
        return jsonify(message="Invalid credentials!"), 401

@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    print(f"Adding book: {data}")
    current_user = get_jwt_identity()
    new_book = Book(title=data['title'], author=data['author'], genre=data['genre'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(message="Book added successfully!", added_by=current_user)

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_list = [{"id": book.id, "title": book.title, "author": book.author, "genre": book.genre} for book in books]
    print("Fetching all books")
    return jsonify(books=books_list)

@app.route('/books/genre/<genre>', methods=['GET'])
def get_books_by_genre(genre):
    books = Book.query.filter_by(genre=genre).all()
    books_list = [{"id": book.id, "title": book.title, "author": book.author, "genre": book.genre} for book in books]
    print(f"Fetching books by genre: {genre}")
    return jsonify(books=books_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

