from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from model import db, User, Admin

app = Flask(__name__)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Login Route
@app.route('/login', methods=['POST'], endpoint='login')
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


# Protected Route
@app.route('/protected', methods=['GET'], endpoint='protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Logout Route
@app.route('/logout', methods=['POST'], endpoint='logout')
@jwt_required()
def logout():
    return jsonify(logged_out=True), 200


# Register Route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstname = data.get('firstname', None)
    lastname = data.get('lastname', None)
    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)

    user = User.query.filter_by(username=username).first()
    if user:
        return make_response('User already exists!', 409, {'WWW-Authenticate': 'Basic realm="Register required!"'})
    else:
        new_user = User(firstname=firstname, lastname=lastname, username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message='User created successfully!'), 201


# User Profile Route
@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_identity = get_jwt_identity()

    user = User.query.filter_by(username=current_identity).first()
    if user:
        user_data = {
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active
        }
        return jsonify(user_data), 200

    admin = Admin.query.filter_by(username=current_identity).first()
    if admin:
        admin_data = {
            'id': admin.id,
            'firstname': admin.firstname,
            'lastname': admin.lastname,
            'username': admin.username,
            'email': admin.email,
            'is_active': admin.is_active
        }
        return jsonify(admin_data), 200

    return jsonify(message="Profile not found"), 404


# Get All Users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'is_active': user.is_active
        }
        user_list.append(user_data)
    return jsonify(user_list), 200


# Get a Single User by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        user_data = {
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'is_active': user.is_active
        }
        return jsonify(user_data), 200
    else:
        return jsonify('User not found!'), 404


# Update User
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if user:
        user.firstname = data.get('firstname', user.firstname)
        user.lastname = data.get('lastname', user.lastname)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.set_password(data.get('password'))
        db.session.commit()
        return jsonify(message='User updated successfully!'), 200
    else:
        return jsonify(message='User not found'), 404


# Delete User
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify('User deleted successfully!'), 200
    else:
        return jsonify('User not found!'), 404


# Get All Admins
@app.route('/admins', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    admin_list = []
    for admin in admins:
        admin_data = {
            'id': admin.id,
            'firstname': admin.firstname,
            'lastname': admin.lastname,
            'username': admin.username,
            'email': admin.email,
            'password_hash': admin.password_hash,
            'is_active': admin.is_active
        }
        admin_list.append(admin_data)
    return jsonify(admin_list), 200


# Get a Single Admin by ID
@app.route('/admins/<int:id>', methods=['GET'])
def get_admin(id):
    admin = Admin.query.get(id)
    if admin:
        admin_data = {
            'id': admin.id,
            'firstname': admin.firstname,
            'lastname': admin.lastname,
            'username': admin.username,
            'email': admin.email,
            'password_hash': admin.password_hash,
            'is_active': admin.is_active
        }
        return jsonify(admin_data), 200
    else:
        return jsonify(message='Admin not found!'), 404


# Update Admin
@app.route('/admin/<int:id>', methods=['PUT'])
def update_admin(id):
    data = request.get_json()
    admin = Admin.query.get(id)
    if admin:
        admin.firstname = data.get('firstname', admin.firstname)
        admin.lastname = data.get('lastname', admin.lastname)
        admin.username = data.get('username', admin.username)
        admin.email = data.get('email', admin.email)
        admin.set_password(data.get('password'))
        db.session.commit()
        return jsonify(message='Admin updated successfully!'), 200
    else:
        return jsonify(message='Admin not found'), 404


# Delete Admin
@app.route('/admin/<int:id>', methods=['DELETE'])
def delete_admin(id):
    admin = Admin.query.get(id)
    if admin:
        db.session.delete(admin)
        db.session.commit()
        return jsonify(message='Admin deleted successfully!'), 200
    else:
        return jsonify(message='Admin not found!'), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
