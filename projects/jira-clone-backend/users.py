from quart import request, jsonify, Blueprint
from model import UsersModel
from db import db_create_user, db_list_users, db_retrieve_user, db_update_user, db_delete_user, db_list_user_tasks
from werkzeug.security import generate_password_hash
from pydantic.error_wrappers import ValidationError


users = Blueprint('users', __name__)


@users.errorhandler(ValidationError)
async def handle_bad_request(e):
    msg = "\n".join( [ f"Provide proper data for {getattr( e.model, error['loc'][0] ).title}, {error['msg']}." for error in e.errors() ] )
    return jsonify({"message": msg, "success": False}), 400


@users.route("/create", methods=["POST"])
async def create_user():
    """"
    Create a new user
    """
    payload = await request.get_json()
    if "id" in payload:    # user cannot pass id when creating a new user
        payload.pop("id")
    
    payload["password"] = generate_password_hash(payload.get("password", ""), method='sha256')
    
    user = UsersModel.from_dict(payload)
    await db_create_user(user)
    return jsonify(data=user.to_dict(exclude = ( 'password', ))), 201


@users.route("/", methods=["GET"])
async def list_user():
    """"
    Retrieve all users
    """
    users = await db_list_users()
    res = {"list": [user.to_dict(exclude = ( 'password', )) for user in users], "count": len(users)}
    return jsonify(data=res), 200


@users.route("/tasks", methods=["GET"])
async def list_user_tasks():
    """"
    Retrieve a user's all tasks
    """
    user_id = request.args.get("id")

    user = await db_retrieve_user(user_id)
    if not user:
        return jsonify({"message": "user not found"}), 404

    tasks = await db_list_user_tasks(user_id)
    res = {"list": [task.to_dict() for task in tasks], "count": len(tasks)}
    return jsonify(data=res), 200


@users.route("/retrieve", methods=["GET"])
async def retrieve_user():
    """"
    Retrieve a user
    """
    user_id = request.args.get("id")
    user = await db_retrieve_user(user_id)
    if user:
        return jsonify(data=user.to_dict(exclude = ( 'password', ))), 200
    return jsonify({"message": "user not found"}), 404


@users.route("/update", methods=["POST"])
async def update_user():
    """"
    Update a user
    """
    payload = await request.get_json()
    
    payload["password"] = generate_password_hash(payload.get("password", ""), method='sha256')
    
    user_id = payload.get("id")
    if not await db_retrieve_user(user_id):
        return jsonify({"message": "user not found"}), 404

    success = await db_update_user(user_id, payload)
    if not success:
        return jsonify({"message": "user Update failed"}), 404
    user_db = await db_retrieve_user(user_id)
    return jsonify(data=user_db.to_dict(exclude = ( 'password', ))), 200


@users.route("/delete", methods=["DELETE"])
async def delete_user():
    """"
    Delete a user
    """
    user_id = request.args.get("id")
    if not user_id:
        return jsonify({"message": "user id is required"}), 400
    success = await db_delete_user(user_id)
    if not success:
        return jsonify({"message": "user Delete failed"}), 404
    return jsonify({"message": "user Deleted"}), 200
