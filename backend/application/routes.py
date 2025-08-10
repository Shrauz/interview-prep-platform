from flask import current_app as app, jsonify, request, render_template, send_from_directory
from flask_security import auth_required,roles_required, roles_accepted, current_user,hash_password,login_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from application.models import db

@app.route("/")
def index():
    return "HELLO ♥"

# gets the current user
@app.route('/api/user', methods=['GET'])
@auth_required('token')
@roles_accepted('user','admin')
def get_user():
    user = current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "email": user.email,
    })
    
@app.route('/api/login', methods=['POST'])
def user_login():
    body = request.get_json()
    email = body['email']
    password = body['password']
    
    if not email:
        return jsonify({'message': 'Email is required'}), 400
    
    user = app.security.datastore.find_user(email=email)
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return jsonify({
                'message': 'Logged in successfully',
                "id": user.id,
                "email": user.email,
                "role": user.roles[0].name,
                "auth-token": user.get_auth_token()
            })
        else:
            return jsonify({'message': 'Invalid password'}), 400
    else:
        return jsonify({'message': 'User not found'}), 404
    

@app.route('/api/logout', methods = ['POST'])
@auth_required('token')
def user_logout():
    user = current_user
    logout_user()
    return jsonify({
        "message": "User logged out"
    })
    

@app.route('/api/register', methods=['POST'])
def create_user():
    credentials = request.get_json()

    # Check if user already exists
    if app.security.datastore.find_user(email=credentials["email"]):
        return jsonify({"message": "User already exists!"}), 400
    
    required_fields = ["email","password"]
    if not all(credentials.get(field) for field in required_fields):
        return jsonify({"message": "All fields are required!"}), 400
        
    app.security.datastore.create_user(
        email=credentials["email"],
        password=generate_password_hash(credentials["password"]),
        roles=['user']
    )
    db.session.commit()

    return jsonify({"message": "User created successfully!"}), 201