from flask import request, jsonify, Blueprint
from model import TasksModel
from db import db_retrieve_user, \
db_create_task, db_list_tasks, db_retrieve_task, db_update_task, db_delete_task, db_list_task_comments
from util import mail


tasks = Blueprint('tasks', __name__)


@tasks.route("/create", methods=["POST"])
def create_task():
    """"
    Create a new task
    """
    payload = request.get_json()
    if "id" in payload:    # user cannot pass id when creating a new task
        payload.pop("id")
    status = TasksModel.Schema().validate(payload, partial=("id",))   # no validation to id
    if status:
        return jsonify(status), 400
    
    if not db_retrieve_user( payload.get("reporter") ):
        return jsonify({"message": "reporter user not found"}), 404
    
    if not db_retrieve_user( payload.get("assignee") ):
        return jsonify({"message": "assignee user not found"}), 404
    
    task = TasksModel.from_dict(payload)
    db_create_task(task)

    if payload.get("reporter") != payload.get("assignee"):
        mail(f"{ db_retrieve_user(payload.get('assignee')).to_dict().get('email') }",
             f"New Task { payload.get('title')[:10] } by {db_retrieve_user(payload.get('reporter')).to_dict().get('name') }",
             f"New Task { payload.get('title') } by {payload.get('reporter')} Details: {payload.get('description') }")

    return jsonify(data=task.to_dict()), 201


@tasks.route("/", methods=["GET"])
def list_task():
    """"
    Retrieve all tasks
    """
    tasks = db_list_tasks()
    res = {"list": [task.to_dict() for task in tasks], "count": len(tasks)}
    return jsonify(data=res), 200


@tasks.route("/comments", methods=["GET"])
def list_task_comments():
    """"
    Retrieve a task's all comments
    """
    task_id = request.args.get("id")

    task = db_retrieve_task(task_id)
    if not task:
        return jsonify({"message": "task not found"}), 404

    tasks = db_list_task_comments(task_id)
    res = {"list": [task.to_dict() for task in tasks], "count": len(tasks)}
    return jsonify(data=res), 200


@tasks.route("/retrieve", methods=["GET"])
def retrieve_task():
    """"
    Retrieve a task
    """
    task_id = request.args.get("id")
    task = db_retrieve_task(task_id)
    if task:
        return jsonify(data=task.to_dict()), 200
    return jsonify({"message": "task not found"}), 404


@tasks.route("/update", methods=["POST"])
def update_task():
    """"
    Update a task
    """
    payload = request.get_json()

    old_task = db_retrieve_task( payload.get("id") )
    if old_task:
        payload["reporter"] = old_task.to_dict().get("reporter")
    
    status = TasksModel.Schema().validate(payload)
    if status:
        return jsonify(status), 400
    task_id = payload.get("id")
    if not db_retrieve_task(task_id):
        return jsonify({"message": "task not found"}), 404

    task_db = db_retrieve_task(task_id)
    old_task = task_db.to_dict()

    success = db_update_task(task_id, payload)
    if not success:
        return jsonify({"message": "task Update failed"}), 404
    task_db = db_retrieve_task(task_id)

    if task_db.to_dict().get("reporter") != task_db.to_dict().get("assignee") and old_task.get("assignee") != task_db.to_dict().get("assignee"):
        mail(f"{ db_retrieve_user(payload.get('assignee')).to_dict().get('email') }",
             f"New Task { payload.get('title')[:10] } by {db_retrieve_user(payload.get('reporter')).to_dict().get('name') }",
             f"New Task { payload.get('title') } by {payload.get('reporter')} Details: {payload.get('description') }")

    return jsonify(data=task_db.to_dict()), 200


@tasks.route("/delete", methods=["DELETE"])
def delete_task():
    """"
    Delete a task
    """
    task_id = request.args.get("id")
    if not task_id:
        return jsonify({"message": "task id is required"}), 400
    success = db_delete_task(task_id)
    if not success:
        return jsonify({"message": "task Delete failed"}), 404
    return jsonify({"message": "task Deleted"}), 200
