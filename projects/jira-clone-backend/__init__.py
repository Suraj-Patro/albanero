from flask import Flask, request, jsonify
from model import UsersModel, TasksModel, CommentsModel
from db import db_create_user, db_list_users, db_retrieve_user, db_update_user, db_delete_user, db_list_user_tasks, \
db_create_task, db_list_tasks, db_retrieve_task, db_update_task, db_delete_task, db_list_task_comments, \
db_create_comment, db_list_comments, db_retrieve_comment, db_update_comment, db_delete_comment
from util import mail

app = Flask(__name__)


# Users Endpoint
@app.route("/users/create", methods=["POST"])
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


@app.route("/users/", methods=["GET"])
def list_user():
    """"
    Retrieve all users
    """
    users = db_list_users()
    res = {"list": [user.to_dict() for user in users], "count": len(users)}
    return jsonify(data=res), 200


@app.route("/users/tasks", methods=["GET"])
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


@app.route("/users/retrieve", methods=["GET"])
def retrieve_user():
    """"
    Retrieve a user
    """
    user_id = request.args.get("id")
    user = db_retrieve_user(user_id)
    if user:
        return jsonify(data=user.to_dict()), 200
    return jsonify({"message": "user not found"}), 404


@app.route("/users/update", methods=["POST"])
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


@app.route("/users/delete", methods=["DELETE"])
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



# Tasks Endpoint
@app.route("/tasks/create", methods=["POST"])
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


@app.route("/tasks/", methods=["GET"])
def list_task():
    """"
    Retrieve all tasks
    """
    tasks = db_list_tasks()
    res = {"list": [task.to_dict() for task in tasks], "count": len(tasks)}
    return jsonify(data=res), 200


@app.route("/tasks/comments", methods=["GET"])
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


@app.route("/tasks/retrieve", methods=["GET"])
def retrieve_task():
    """"
    Retrieve a task
    """
    task_id = request.args.get("id")
    task = db_retrieve_task(task_id)
    if task:
        return jsonify(data=task.to_dict()), 200
    return jsonify({"message": "task not found"}), 404


@app.route("/tasks/update", methods=["POST"])
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


@app.route("/tasks/delete", methods=["DELETE"])
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


# Comments Endpoint
@app.route("/comments/create", methods=["POST"])
def create_comment():
    """"
    Create a new comment
    """
    payload = request.get_json()
    if "id" in payload:    # user cannot pass id when creating a new comment
        payload.pop("id")
    status = CommentsModel.Schema().validate(payload, partial=("id",))   # no validation to id
    if status:
        return jsonify(status), 400
    
    if not db_retrieve_user( payload.get("user") ):
        return jsonify({"message": "user not found"}), 404
    
    if not db_retrieve_task( payload.get("task") ):
        return jsonify({"message": "task not found"}), 404
    
    comment = CommentsModel.from_dict(payload)
    db_create_comment(comment)


    _task = db_retrieve_task( payload.get("task") )
    
    if payload.get("user") != _task.to_dict().get("assignee"):
        mail(f"{db_retrieve_user(_task.to_dict().get('assignee')).to_dict().get('email')}",
             f"New Comment { payload.get('message')[:5] } ... by { db_retrieve_user(payload.get('user')).to_dict().get('name') }",
             f"New Comment by { db_retrieve_user(payload.get('user')).to_dict().get('name') } Details: { payload.get('message') }")

    
    if payload.get("user") != _task.to_dict().get("reporter"):
        mail(f"{db_retrieve_user(_task.to_dict().get('reporter')).to_dict().get('email')}",
             f"New Comment { payload.get('message')[:5] } ... by { db_retrieve_user(payload.get('user')).to_dict().get('name') }",
             f"New Comment by { db_retrieve_user(payload.get('user')).to_dict().get('name') } Details: { payload.get('message') }")


    return jsonify(data=comment.to_dict()), 201


@app.route("/comments/", methods=["GET"])
def list_comment():
    """"
    Retrieve all comments
    """
    comments = db_list_comments()
    res = {"list": [comment.to_dict() for comment in comments], "count": len(comments)}
    return jsonify(data=res), 200


@app.route("/comments/retrieve", methods=["GET"])
def retrieve_comment():
    """"
    Retrieve a comment
    """
    comment_id = request.args.get("id")
    comment = db_retrieve_comment(comment_id)
    if comment:
        return jsonify(data=comment.to_dict()), 200
    return jsonify({"message": "comment not found"}), 404


@app.route("/comments/update", methods=["POST"])
def update_comment():
    """"
    Update a comment
    """
    payload = request.get_json()
    
    old_comment = db_retrieve_comment( payload.get("id") )
    if old_comment:
        payload["user"] = old_comment.to_dict().get("user")
        payload["task"] = old_comment.to_dict().get("task")
    
    status = CommentsModel.Schema().validate(payload)
    if status:
        return jsonify(status), 400
    comment_id = payload.get("id")
    if not db_retrieve_comment(comment_id):
        return jsonify({"message": "comment not found"}), 404

    success = db_update_comment(comment_id, payload)
    if not success:
        return jsonify({"message": "comment Update failed"}), 404
    comment_db = db_retrieve_comment(comment_id)

    return jsonify(data=comment_db.to_dict()), 200


@app.route("/comments/delete", methods=["DELETE"])
def delete_comment():
    """"
    Delete a comment
    """
    comment_id = request.args.get("id")
    if not comment_id:
        return jsonify({"message": "comment id is required"}), 400
    success = db_delete_comment(comment_id)
    if not success:
        return jsonify({"message": "comment Delete failed"}), 404
    return jsonify({"message": "comment Deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
