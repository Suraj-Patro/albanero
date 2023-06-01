from quart import request, jsonify, Blueprint
from model import TasksModel
from db import db_retrieve_user, \
db_create_task, db_list_tasks, db_retrieve_task, db_update_task, db_delete_task, db_list_task_comments
from util import mail
from pydantic.error_wrappers import ValidationError


tasks = Blueprint('tasks', __name__)


@tasks.errorhandler(ValidationError)
async def handle_bad_request(e):
    msg = "\n".join( [ f"Provide proper data for {getattr( e.model, error['loc'][0] ).title}, {error['msg']}." for error in e.errors() ] )
    return jsonify({"message": msg, "success": False}), 400


@tasks.route("/create", methods=["POST"])
async def create_task():
    """"
    Create a new task
    """
    payload = await request.get_json()
    if "id" in payload:    # user cannot pass id when creating a new task
        payload.pop("id")
    
    if not await db_retrieve_user( payload.get("reporter") ):
        return jsonify({"message": "reporter user not found"}), 404
    
    if not await db_retrieve_user( payload.get("assignee") ):
        return jsonify({"message": "assignee user not found"}), 404
    
    task = TasksModel.from_dict(payload)
    await db_create_task(task)

    if payload.get("reporter") != payload.get("assignee"):
        await mail(f"{ await db_retrieve_user(payload.get('assignee')).to_dict().get('email') }",
             f"New Task { payload.get('title')[:10] } by {await db_retrieve_user(payload.get('reporter')).to_dict().get('name') }",
             f"New Task { payload.get('title') } by {payload.get('reporter')} Details: {payload.get('description') }")

    return jsonify(data=task.to_dict()), 201


@tasks.route("/", methods=["GET"])
async def list_task():
    """"
    Retrieve all tasks
    """
    tasks = await db_list_tasks()
    res = {"list": [task.to_dict() for task in tasks], "count": len(tasks)}
    return jsonify(data=res), 200


@tasks.route("/comments", methods=["GET"])
async def list_task_comments():
    """"
    Retrieve a task's all comments
    """
    task_id = request.args.get("id")

    task = await db_retrieve_task(task_id)
    if not task:
        return jsonify({"message": "task not found"}), 404

    comments = await db_list_task_comments(task_id)
    res = {"list": [comment.to_dict() for comment in comments], "count": len(comments)}
    return jsonify(data=res), 200


@tasks.route("/retrieve", methods=["GET"])
async def retrieve_task():
    """"
    Retrieve a task
    """
    task_id = request.args.get("id")
    task = await db_retrieve_task(task_id)
    if task:
        return jsonify(data=task.to_dict()), 200
    return jsonify({"message": "task not found"}), 404


@tasks.route("/update", methods=["POST"])
async def update_task():
    """"
    Update a task
    """
    payload = await request.get_json()

    old_task = await db_retrieve_task( payload.get("id") )
    if old_task:
        payload["reporter"] = old_task.to_dict().get("reporter")

    task_id = payload.get("id")
    if not await db_retrieve_task(task_id):
        return jsonify({"message": "task not found"}), 404

    success = await db_update_task(task_id, payload)
    if not success:
        return jsonify({"message": "task Update failed"}), 404
    task_db = await db_retrieve_task(task_id)

    if task_db.to_dict().get("reporter") != task_db.to_dict().get("assignee") and old_task.get("assignee") != task_db.to_dict().get("assignee"):
        await mail(f"{ await db_retrieve_user(payload.get('assignee')).to_dict().get('email') }",
             f"New Task { payload.get('title')[:10] } by {await db_retrieve_user(payload.get('reporter')).to_dict().get('name') }",
             f"New Task { payload.get('title') } by {payload.get('reporter')} Details: {payload.get('description') }")

    return jsonify(data=task_db.to_dict()), 200


@tasks.route("/delete", methods=["DELETE"])
async def delete_task():
    """"
    Delete a task
    """
    task_id = request.args.get("id")
    if not task_id:
        return jsonify({"message": "task id is required"}), 400
    success = await db_delete_task(task_id)
    if not success:
        return jsonify({"message": "task Delete failed"}), 404
    return jsonify({"message": "task Deleted"}), 200
