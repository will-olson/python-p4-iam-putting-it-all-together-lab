from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from models import db, User, Recipe
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Recipe App!"})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 422

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 422

    try:
        new_user = User(
            username=username,
            image_url=data.get('image_url', None),
            bio=data.get('bio', None),
        )
        new_user.password_hash = password
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 422

    user = User.query.filter_by(username=username).first()

    if user and user.authenticate(password):
        session['user_id'] = user.id
        return jsonify({'username': user.username, 'id': user.id}), 200

    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout', methods=['DELETE'])
def logout():
    if session.get('user_id') is None:
        return jsonify({'error': 'Unauthorized'}), 401
    
    session.pop('user_id')
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(session['user_id'])
    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "image_url": user.image_url,
            "bio": user.bio
        }), 200

    return jsonify({"error": "Unauthorized"}), 401

@app.route('/recipes', methods=['GET', 'POST'])
def handle_recipes():
    if not session.get('user_id'): 
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'GET':
        recipes = Recipe.query.filter_by(user_id=session['user_id']).all()
        return jsonify([{
            "id": recipe.id,
            "title": recipe.title,
            "instructions": recipe.instructions,
            "minutes_to_complete": recipe.minutes_to_complete,
            "user_id": recipe.user_id
        } for recipe in recipes]), 200

    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({"error": "Invalid JSON format."}), 400

        if not all(key in data for key in ['title', 'instructions', 'minutes_to_complete']):
            return jsonify({"error": "Missing required fields."}), 422

        try:
            new_recipe = Recipe(
                title=data['title'],
                instructions=data['instructions'],
                minutes_to_complete=data['minutes_to_complete'],
                user_id=session['user_id'],
            )
            db.session.add(new_recipe)
            db.session.commit()

            return jsonify({
                "id": new_recipe.id,
                "title": new_recipe.title,
                "instructions": new_recipe.instructions,
                "minutes_to_complete": new_recipe.minutes_to_complete,
                "user_id": new_recipe.user_id
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)