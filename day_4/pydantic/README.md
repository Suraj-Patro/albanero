from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '123',
    'signup_ts': '2019-06-01 12:22',
    'friends': [1, 2, '3'],
}


try:
    user = User(**external_data)
except ValidationError as e:
    print(e.json())

print(user.id)

print(repr(user.signup_ts))

print(user.friends)

print(user.dict())
