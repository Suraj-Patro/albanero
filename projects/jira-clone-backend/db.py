import os
import pymongo
from model import *
from typing import List, Dict, Any


client = pymongo.MongoClient( os.getenv("MONGO_CONN_STR", default="mongodb://localhost:27017/") )
Db = client["jira"]
CUsers = Db['users']
CTasks = Db['tasks']
CComments = Db['comments']


# Users
def db_create_user(user: UsersModel) -> bool:
    CUsers.insert_one(user.to_dict())


def db_update_user(user_id: str, user: Dict[str, Any]) -> bool:
    res = CUsers.update_one({"id": user_id}, {"$set": user})
    return res.modified_count > 0


def db_list_users() -> List[UsersModel]:
    return [UsersModel.from_dict(r) for r in CUsers.find()]


def db_list_user_tasks(user_id: str) -> List[TasksModel]:
    return [TasksModel.from_dict(r) for r in CTasks.aggregate( [ { "$match": { "assignee": user_id } } ] )]


def db_retrieve_user(user_id: str) -> UsersModel:
    _user = CUsers.find_one({"id": user_id})
    return UsersModel.from_dict(_user) if _user else None


def db_delete_user(user_id: str) -> bool:
    res = CUsers.delete_one({"id": user_id})
    return res.deleted_count > 0


# Tasks
def db_create_task(task: TasksModel) -> bool:
    CTasks.insert_one(task.to_dict())


def db_update_task(task_id: str, task: Dict[str, Any]) -> bool:
    res = CTasks.update_one({"id": task_id}, {"$set": task})
    return res.modified_count > 0


def db_list_tasks() -> List[TasksModel]:
    return [TasksModel.from_dict(r) for r in CTasks.find()]


def db_list_task_comments(task_id: str) -> List[CommentsModel]:
    return [CommentsModel.from_dict(r) for r in CComments.aggregate( [ { "$match": { "task": task_id } } ] )]


def db_retrieve_task(task_id: str) -> TasksModel:
    _task = CTasks.find_one({"id": task_id})
    return TasksModel.from_dict(_task) if _task else None


def db_delete_task(task_id: str) -> bool:
    res = CTasks.delete_one({"id": task_id})
    return res.deleted_count > 0


# Comments
def db_create_comment(comment: CommentsModel) -> bool:
    CComments.insert_one(comment.to_dict())


def db_update_comment(comment_id: str, comment: Dict[str, Any]) -> bool:
    res = CComments.update_one({"id": comment_id}, {"$set": comment})
    return res.modified_count > 0


def db_list_comments() -> List[CommentsModel]:
    return [CommentsModel.from_dict(r) for r in CComments.find()]


def db_retrieve_comment(comment_id: str) -> CommentsModel:
    _comment = CComments.find_one({"id": comment_id})
    return CommentsModel.from_dict(_comment) if _comment else None


def db_delete_comment(comment_id: str) -> bool:
    res = CComments.delete_one({"id": comment_id})
    return res.deleted_count > 0
