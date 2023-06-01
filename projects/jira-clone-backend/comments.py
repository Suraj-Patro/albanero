from quart import request, jsonify, Blueprint
from model import CommentsModel
from db import db_retrieve_user, \
    db_retrieve_task, \
db_create_comment, db_list_comments, db_retrieve_comment, db_update_comment, db_delete_comment
from util import mail
from pydantic.error_wrappers import ValidationError


comments = Blueprint('comments', __name__)


@comments.errorhandler(ValidationError)
async def handle_bad_request(e):
    msg = "\n".join( [ f"Provide proper data for {getattr( e.model, error['loc'][0] ).title}, {error['msg']}." for error in e.errors() ] )
    return jsonify({"message": msg, "success": False}), 400


@comments.route("/create", methods=["POST"])
async def create_comment():
    """"
    Create a new comment
    """
    payload = await request.get_json()
    if "id" in payload:    # user cannot pass id when creating a new comment
        payload.pop("id")
    
    if not await db_retrieve_user( payload.get("user") ):
        return jsonify({"message": "user not found"}), 404
    
    if not await db_retrieve_task( payload.get("task") ):
        return jsonify({"message": "task not found"}), 404
    
    comment = CommentsModel.from_dict(payload)
    await db_create_comment(comment)


    _task = await db_retrieve_task( payload.get("task") )
    
    recipient = ""

    if payload.get("user") != _task.to_dict().get("assignee"):
        recipient = "assignee"
    
    if payload.get("user") != _task.to_dict().get("reporter"):
        recipient = "reporter"

    if recipient:
        await mail(f"{await db_retrieve_user(_task.to_dict().get( recipient )).to_dict().get('email')}",
            f"New Comment { payload.get('message')[:5] } ... by { await db_retrieve_user(payload.get('user')).to_dict().get('name') }",
            f"New Comment by { await db_retrieve_user(payload.get('user')).to_dict().get('name') } Details: { payload.get('message') }")

    return jsonify(data=comment.to_dict()), 201


@comments.route("/", methods=["GET"])
async def list_comment():
    """"
    Retrieve all comments
    """
    comments = await db_list_comments()
    res = {"list": [comment.to_dict() for comment in comments], "count": len(comments)}
    return jsonify(data=res), 200


@comments.route("/retrieve", methods=["GET"])
async def retrieve_comment():
    """"
    Retrieve a comment
    """
    comment_id = request.args.get("id")
    comment = await db_retrieve_comment(comment_id)
    if comment:
        return jsonify(data=comment.to_dict()), 200
    return jsonify({"message": "comment not found"}), 404


@comments.route("/update", methods=["POST"])
async def update_comment():
    """"
    Update a comment
    """
    payload = await request.get_json()
    
    old_comment = await db_retrieve_comment( payload.get("id") )
    if old_comment:
        payload["user"] = old_comment.to_dict().get("user")
        payload["task"] = old_comment.to_dict().get("task")
    
    comment_id = payload.get("id")
    if not await db_retrieve_comment(comment_id):
        return jsonify({"message": "comment not found"}), 404

    success = await db_update_comment(comment_id, payload)
    if not success:
        return jsonify({"message": "comment Update failed"}), 404
    comment_db = await db_retrieve_comment(comment_id)

    return jsonify(data=comment_db.to_dict()), 200


@comments.route("/delete", methods=["DELETE"])
async def delete_comment():
    """"
    Delete a comment
    """
    comment_id = request.args.get("id")
    if not comment_id:
        return jsonify({"message": "comment id is required"}), 400
    success = await db_delete_comment(comment_id)
    if not success:
        return jsonify({"message": "comment Delete failed"}), 404
    return jsonify({"message": "comment Deleted"}), 200
