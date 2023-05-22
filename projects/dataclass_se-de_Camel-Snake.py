from __future__ import annotations  # This can be removed in Python 3.10+
from dataclasses import dataclass, field
from datetime import date
from enum import Enum

from dataclass_wizard import JSONWizard


@dataclass
class Data(JSONWizard):

    class _(JSONWizard.Meta):
        # Sets the target key transform to use for serialization;
        # defaults to `camelCase` if not specified.
        key_transform_with_dump = 'LISP'

    a_sample_bool: bool
    values: list[Inner] = field(default_factory=list)


@dataclass
class Inner:
    vehicle: Car | None
    my_dates: dict[int, date]


class Car(Enum):
    SEDAN = 'BMW Coupe'
    SUV = 'Toyota 4Runner'
    JEEP = 'Jeep Cherokee'


def main():

    my_dict = {
        'values': [
            {
                'vehicle': 'Toyota 4Runner',
                'My-Dates': {'123': '2023-01-31'}
            },
            {
                'vehicle': None,
                'my_dates': {}
            }
        ],
        'aSampleBool': 'TRUE'
    }

    # De-serialize (a JSON string or dictionary data) into a `Data` instance.
    data = Data.from_dict(my_dict)

    print(repr(data))
    # > Data(a_sample_bool=True, values=[Inner(vehicle=<Car.SUV: 'Toyota 4Runner'>, ...)])

    # assert enums values are as expected
    print(data.values[0].vehicle is Car.SUV)

    print(data.to_json(indent=2))
    # {
    #   "a-sample-bool": true,
    #   "values": [
    #     {
    #       "vehicle": "Toyota 4Runner",
    #       "my-dates": {
    #         "123": "2023-01-31"
    #       },
    #   ...

    # True
    print(data == data.from_json(data.to_json()))

if __name__ == '__main__':
    main()
