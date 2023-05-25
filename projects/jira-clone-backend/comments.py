from flask import request, jsonify, Blueprint
from model import CommentsModel
from db import db_retrieve_user, \
    db_retrieve_task, \
db_create_comment, db_list_comments, db_retrieve_comment, db_update_comment, db_delete_comment
from util import mail


comments = Blueprint('comments', __name__)


@comments.route("/create", methods=["POST"])
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
    
    recipient = ""

    if payload.get("user") != _task.to_dict().get("assignee"):
        recipient = "assignee"
    
    if payload.get("user") != _task.to_dict().get("reporter"):
        recipient = "reporter"

    if recipient:
        mail(f"{db_retrieve_user(_task.to_dict().get( recipient )).to_dict().get('email')}",
            f"New Comment { payload.get('message')[:5] } ... by { db_retrieve_user(payload.get('user')).to_dict().get('name') }",
            f"New Comment by { db_retrieve_user(payload.get('user')).to_dict().get('name') } Details: { payload.get('message') }")

    return jsonify(data=comment.to_dict()), 201


@comments.route("/", methods=["GET"])
def list_comment():
    """"
    Retrieve all comments
    """
    comments = db_list_comments()
    res = {"list": [comment.to_dict() for comment in comments], "count": len(comments)}
    return jsonify(data=res), 200


@comments.route("/retrieve", methods=["GET"])
def retrieve_comment():
    """"
    Retrieve a comment
    """
    comment_id = request.args.get("id")
    comment = db_retrieve_comment(comment_id)
    if comment:
        return jsonify(data=comment.to_dict()), 200
    return jsonify({"message": "comment not found"}), 404


@comments.route("/update", methods=["POST"])
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


@comments.route("/delete", methods=["DELETE"])
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
