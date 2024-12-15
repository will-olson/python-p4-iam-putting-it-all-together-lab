from flask import Flask, jsonify, request
from models import db, User, Recipe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Recipe App!"})

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([{
            "id": user.id,
            "username": user.username,
            "image_url": user.image_url,
            "bio": user.bio
        } for user in users])
    
    if request.method == 'POST':
        data = request.get_json()
        try:
            new_user = User(
                username=data['username'],
                image_url=data.get('image_url', None),
                bio=data.get('bio', None),
            )
            new_user.password_hash = data['password']
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User created successfully."}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

@app.route('/recipes', methods=['GET', 'POST'])
def handle_recipes():
    if request.method == 'GET':
        recipes = Recipe.query.all()
        return jsonify([{
            "id": recipe.id,
            "title": recipe.title,
            "instructions": recipe.instructions,
            "minutes_to_complete": recipe.minutes_to_complete,
            "user_id": recipe.user_id
        } for recipe in recipes])
    
    if request.method == 'POST':
        data = request.get_json()
        try:
            new_recipe = Recipe(
                title=data['title'],
                instructions=data['instructions'],
                minutes_to_complete=data['minutes_to_complete'],
                user_id=data.get('user_id', None),
            )
            db.session.add(new_recipe)
            db.session.commit()
            return jsonify({"message": "Recipe created successfully."}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)