import uuid
from dataclasses import field
from marshmallow_dataclass import dataclass as mm_dataclass
from dataclasses_json import dataclass_json, Undefined
from marshmallow import validate
from flask_login import UserMixin


@dataclass_json(undefined=Undefined.EXCLUDE)
@mm_dataclass(frozen=True)
class UsersModel(UserMixin):
    username: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    name: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    email: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    password: str = field(metadata={"validate": validate.Length(equal=88)})
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass_json(undefined=Undefined.EXCLUDE)
@mm_dataclass(frozen=True)
class TasksModel(UserMixin):
    title: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    description: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    reporter: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    assignee: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass_json(undefined=Undefined.EXCLUDE)
@mm_dataclass(frozen=True)
class CommentsModel(UserMixin):
    message: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    task: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    user: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
