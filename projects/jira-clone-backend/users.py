from flask import request, jsonify, Blueprint
from model import UsersModel
from db import db_create_user, db_list_users, db_retrieve_user, db_update_user, db_delete_user, db_list_user_tasks


users = Blueprint('users', __name__)


@users.route("/create", methods=["POST"])
def create_user():
    """"
    Create a new user
    """
    payload = request.get_json()
    if "id" in payload:    # user cannot pass id when creating a new user
        payload.pop("id")
    status = UsersModel.Schema().validate(payload, partial=("id",))   # no validation to id
    if status:
        return jsonify(status), 400
    user = UsersModel.from_dict(payload)
    db_create_user(user)
    return jsonify(data=user.to_dict()), 201


@users.route("/", methods=["GET"])
def list_user():
    """"
    Retrieve all users
    """
    users = db_list_users()
    res = {"list": [user.to_dict() for user in users], "count": len(users)}
    return jsonify(data=res), 200


@users.route("/tasks", methods=["GET"])
def list_user_tasks():
    """"
    Retrieve a user all tasks
    """
    user_id = request.args.get("id")

    user = db_retrieve_user(user_id)
    if not user:
        return jsonify({"message": "user not found"}), 404

    tasks = db_list_user_tasks(user_id)
    res = {"list": [user.to_dict() for user in tasks], "count": len(tasks)}
    return jsonify(data=res), 200


@users.route("/retrieve", methods=["GET"])
def retrieve_user():
    """"
    Retrieve a user
    """
    user_id = request.args.get("id")
    user = db_retrieve_user(user_id)
    if user:
        return jsonify(data=user.to_dict()), 200
    return jsonify({"message": "user not found"}), 404


@users.route("/update", methods=["POST"])
def update_user():
    """"
    Update a user
    """
    payload = request.get_json()
    
    status = UsersModel.Schema().validate(payload)
    if status:
        return jsonify(status), 400
    user_id = payload.get("id")
    if not db_retrieve_user(user_id):
        return jsonify({"message": "user not found"}), 404

    success = db_update_user(user_id, payload)
    if not success:
        return jsonify({"message": "user Update failed"}), 404
    user_db = db_retrieve_user(user_id)
    return jsonify(data=user_db.to_dict()), 200


@users.route("/delete", methods=["DELETE"])
def delete_user():
    """"
    Delete a user
    """
    user_id = request.args.get("id")
    if not user_id:
        return jsonify({"message": "user id is required"}), 400
    success = db_delete_user(user_id)
    if not success:
        return jsonify({"message": "user Delete failed"}), 404
    return jsonify({"message": "user Deleted"}), 200
