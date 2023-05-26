from typing import List, Optional

from pydantic.dataclasses import dataclass

import dataclasses
from pydantic import Field

from dataclass_wizard import JSONSerializable


@dataclass
class User(JSONSerializable):
    id_value: int
    name_value: str = 'John Doe'
    friends_value: List[int] = dataclasses.field(default_factory=lambda: [0])
    age_value: Optional[int] = dataclasses.field(
        default=None,
        metadata = { "title": "The age of the user", "description": "do not lie!" }
    )
    height_value: Optional[int] = Field(None, title='The height in cm', ge=50, le=300)


try:
    User(id_value=10, height_value=10)
except Exception as e:
    print(e)
    print(type(e))
    print(type(e).__name__)
    print(e.args)
    print(e.with_traceback)
