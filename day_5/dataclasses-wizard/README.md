IMP:

https://dataclass-wizard.readthedocs.io/en/latest/common_use_cases/serialization_options.html#exclude-fields



set of simple
    elegant wizarding tools for interacting with the Python dataclasses module
    fast serialization framework
        enables dataclass instances to be converted to/from JSON
        works well with a nested dataclass model



from __future__ import annotations

from dataclasses import dataclass, field

from dataclass_wizard import JSONWizard


@dataclass

class MyClass(JSONWizard):

    my_str: str | None

    is_active_tuple: tuple[bool, ...]

    list_of_int: list[int] = field(default_factory=list)


string = """

{

  "my_str": 20,

  "ListOfInt": ["1", "2", 3],

  "isActiveTuple": ["true", false, 1]

}

"""


instance = MyClass.from_json(string)

instance
MyClass(my_str='20', is_active_tuple=(True, False, True), list_of_int=[1, 2, 3])

instance.to_json()
'{"myStr": "20", "isActiveTuple": [true, false, true], "listOfInt": [1, 2, 3]}'

instance == MyClass.from_dict(instance.to_dict())
True

