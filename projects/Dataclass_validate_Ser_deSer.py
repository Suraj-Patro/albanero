from typing import List, Optional

from pydantic.dataclasses import dataclass

import dataclasses
from pydantic import Field

from dataclass_wizard import JSONSerializable


@dataclass
class User(JSONSerializable):
    id_value: int
    name_value: str = 'John Doe'
    # friends_value: List[int] = dataclasses.field(default_factory=lambda: [0])
    # age_value: Optional[int] = dataclasses.field(
    #     default=None,
    #     metadata = { "title": "The age of the user", "description": "do not lie!" }
    # )
    height_value: Optional[int] = Field(None, title='The height in cm', ge=50, le=300, exclude=True)        # exclude parameter only available in pydantic Field


User(id_value=10, height_value=10)


# try:
#     User(id_value=10, height_value=10)
# except Exception as e:
#     print(e)
    # print(type(e))
    # print(type(e).__name__)
    # print(e.args)
    # print(e.with_traceback)

# user = User(id_value=10, height_value=100)

# # exclusion works with to_dict not with to_json
# user.to_dict( exclude = ( 'id_value', ) )


# # exclusion doesn't work with to_json
# # user.to_json( exclude = ( 'id_value', ) )

# print( json.dumps( user.to_dict( exclude = ( 'id_value', ) ) ) )


# class User(BaseModel):
#     id: int
#     username: str
#     password: str = Field(exclude=True)
#     hobbies: List[str]

# my_user = User(id=42, username='JohnDoe', password='hashedpassword', hobbies=['scuba diving'])

# # my_user._priv = 13
# assert my_user.id == 42
# # assert my_user.password.get_secret_value() == 'hashedpassword'
# assert my_user.dict() == {'id': 42, 'username': 'JohnDoe', 'hobbies': ['scuba diving']}

# print( my_user.dict() )
# print( my_user.json() )
