import uuid
from typing import Optional, List
from datetime import datetime
from pydantic import Field
from pydantic.dataclasses import dataclass
from dataclass_wizard import JSONSerializable


@dataclass
class UsersModel(JSONSerializable):
    user_name: str = Field( title="User Name", min_length=5, max_length=256 )
    name: str = Field( title="Name", min_length=3, max_length=256 )
    email: str = Field( min_length=1, max_length=256 )
    password: str = Field( min_length=88, max_length=88 )
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class TasksModel(JSONSerializable):
    title: str = Field( min_length=1, max_length=256 )
    description: str = Field( min_length=1, max_length=256 )
    reporter: str = Field( min_length=36, max_length=36 )
    assignee: str = Field( min_length=36, max_length=36 )
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class CommentsModel(JSONSerializable):
    message: str = Field( min_length=1, max_length=256 )
    task: str = Field( min_length=36, max_length=36 )
    user: str = Field( min_length=36, max_length=36 )
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
