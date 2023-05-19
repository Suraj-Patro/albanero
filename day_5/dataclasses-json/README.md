
https://pypi.org/project/dataclasses-json/



from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Person:
    name: str


person = Person(name='lidatong')
person.to_json()  # '{"name": "lidatong"}' <- this is a string
person.to_dict()  # {'name': 'lidatong'} <- this is a dict
Person.from_json('{"name": "lidatong"}')  # Person(1)
Person.from_dict({'name': 'lidatong'})  # Person(1)

