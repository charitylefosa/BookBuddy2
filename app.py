from flask import Flask, jsonify, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for ORM
from flask_bcrypt import Bcrypt  # Bcrypt for hashing passwords
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # JWT for authentication

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # SQLite database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for SQLAlchemy
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Secret key for JWT, change this to a random secret key in production

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User model for storing user data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Book model for storing book data
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)

# Home route, returns a welcome message
@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        # Fetch book details from Google Books API
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}')
        if response.status_code == 200:
            books = response.json().get('items', [])
        else:
            books = []
    else:
        books = None
    return render_template('search.html', books=books)

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get JSON data from request
    print(f"Registering user: {data}")
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')  # Hash the user's password
    new_user = User(username=data['username'], password=hashed_password)  # Create a new user instance
    db.session.add(new_user)  # Add new user to the database
    db.session.commit()  # Commit changes to the database
    return jsonify(message="User registered successfully!")  # Return success message

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get JSON data from request
    print(f"Login attempt: {data}")
    user = User.query.filter_by(username=data['username']).first()  # Query user by username
    if user and bcrypt.check_password_hash(user.password, data['password']):  # Check password
        access_token = create_access_token(identity={'username': user.username})  # Create JWT access token
        return jsonify(access_token=access_token)  # Return access token
    else:
        return jsonify(message="Invalid credentials!"), 401  # Return error message if credentials are invalid

# Route for adding a new book (requires authentication)
@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()  # Get JSON data from request
    print(f"Adding book: {data}")
    current_user = get_jwt_identity()  # Get current user's identity from JWT
    new_book = Book(title=data['title'], author=data['author'], genre=data['genre'])  # Create a new book instance
    db.session.add(new_book)  # Add new book to the database
    db.session.commit()  # Commit changes to the database
    return jsonify(message="Book added successfully!", added_by=current_user)  # Return success message

# Route for fetching all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()  # Query all books
    books_list = [{"id": book.id, "title": book.title, "author": book.author, "genre": book.genre} for book in books]  # Convert book data to list of dictionaries
    print("Fetching all books")
    return jsonify(books=books_list)  # Return list of books

# Route for fetching books by genre
@app.route('/books/genre/<genre>', methods=['GET'])
def get_books_by_genre(genre):
    books = Book.query.filter_by(genre=genre).all()  # Query books by genre
    books_list = [{"id": book.id, "title": book.title, "author": book.author, "genre": book.genre} for book in books]  # Convert book data to list of dictionaries
    print(f"Fetching books by genre: {genre}")
    return jsonify(books=books_list)  # Return list of books by genre

# Main - run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables
    app.run(debug=True)  # Run the Flask app in debug mode
