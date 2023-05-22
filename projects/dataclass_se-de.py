from __future__ import annotations
from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard


@dataclass
class DataClass(JSONWizard):
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


dc = DataClass.from_json(string)

print(dc)

print(dc.to_json())

print(dc == DataClass.from_dict(dc.to_dict()))
