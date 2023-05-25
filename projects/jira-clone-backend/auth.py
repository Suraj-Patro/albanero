from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from model import UsersModel
from db import db_create_user, db_retrieve_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login_post():
    user_id = request.get_json().get('user_id')
    password = request.get_json().get('password')
    
    # Logic to find if a user is present or not
    user = db_retrieve_user(user_id)

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in DB
    if not user or not check_password_hash(user.to_dict()["password"], password):
        return jsonify({"message": "user Login failed"}), 404
        # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=True)
    return jsonify({"message": "user Login successful"}), 404


@auth.route('/signup', methods=['POST'])
def signup_post():
    """"
    Create a new user
    """
    payload = request.get_json()
    if "id" in payload:    # user cannot pass id when creating a new user
        payload.pop("id")
    
    # Logic to find if a user is present or not
    # give message user already exist

    payload["password"] = generate_password_hash(payload.get("password", ""), method='sha256')
    
    # no validation to id
    status = UsersModel.Schema().validate(payload, partial=("id",))
    if status:
        return jsonify(status), 400
    user = UsersModel.from_dict(payload)
    db_create_user(user)
    return jsonify(data=user.to_dict()), 201


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "user logged out successfully"}), 200
