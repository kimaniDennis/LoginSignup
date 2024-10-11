from flask import Flask,jsonify,make_response,request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import JWTManager,jwt_required,create_access_token,get_jwt_identity
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db,User


app = Flask(__name__)
migrate = Migrate(app,db)
jwt = JWTManager(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serever.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/login', methods=['POST'], endpoint='login')
def login():
    data = request.get_json()
    username  = data.get('username', None)
    password = data.get('password', None)

    user = User.query.filter_by(username=username) .first()

    if user:
        if check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token),200
        else:
            return make_response('Could not verify!', 401,{'WWW-Authenticate':'Basic realm="Login required!"'})
        

@app.route('/protected', methods=['GET'], endpoint='protected')
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user),200


@app.route('/logout', methods=['POST'], endpoint='logout')
@jwt_required
def logout():
    return jsonify(logged_out=True), 200


@app.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    firstname = data.get('firstname', None)
    lastname = data.get('lastname',None)
    username = data.get('username',None)
    email = data.get('username',None)
    password = data.get('password', None)


    # check if the user already exists
    user = User.query.filter_by(username=username).first()
    if user:
        return make_response('User already exists!',409,{'WWW-Authenticate':'Basic realm="Register required!"'})
    else:

        new_user = User(firstname=firstname,lastname=lastname,username=username,email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message='User created successfully!'),201
    

@app.route('/users',methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id':user.id,
            'firstname':user.firstname,
            'lastname':user.lastname,
            'username':user.username,
            'email':user.email,
            'password_hash':user.password_hash,
            'is_active':user.is_active
        }
        user_list.append(user_data)
        return jsonify(user_list),200
    

@app.route('/users/<int:id>',methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        user_data = {
            'id':user.id,
            'firstname':user.firstname,
            'lastname':user.lastname,
            'username':user.username,
            'email':user.email,
            'password_hash':user.password_hash,
            'is_active':user.is_active
        }
        return jsonify(user_data),200
    else:
        return jsonify('User not found!', 404, {'WWW-Authenticate': 'Basic realm="User not found!"'})
    

@app.route('/user/<int:id>', methods = ['PUT'])
def update_user(id):
    data = request.get_json()
    user =  User.query.get(id)
    if user:
        user.firstname = data.get('firstname', user.firstname)
        user.lastname = data.get('lastname', user.lastname)
        user.username = data.get('username',user.username)
        user.email = data.get('email',user.email)
        user.set_password(data.get('password'))
        db.session.commit()
        return jsonify(message = 'User updated successfully!'),200
    else:
        return jsonify(message = 'User not found'),404
    

@app.route('user/<int:id>', methods = ['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify('User deleted successfully!',200)
    else:
        return jsonify('User not found!', 404, {'WWW-Authenticate': 'Basic realm="User not found!"'})
    

    
    