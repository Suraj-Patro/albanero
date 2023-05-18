dataclasses
    provides a decorator and functions
    for automatically adding generated special methods to user-defined classes
    - __init__()
    - __repr__()
    
    member variables to use in these generated methods are defined using PEP 526 type annotations


from dataclasses import dataclass

@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand


will automatically add method

def __init__(self, name: str, unit_price: float, quantity_on_hand: int = 0):
    self.name = name
    self.unit_price = unit_price
    self.quantity_on_hand = quantity_on_hand


2 exceptions
    no datatype validation as per variable annotation
    order of the fields in all of the generated methods
    same as the class definition order
    dataclass() decorator will add various “dunder” methods to the class
        If any of the added methods already exist in the class
            behavior depends on the parameter
    decorator returns the same class that it is called on
        no new class is created
    
    used with no parameters
        acts as if it has the default values documented in this signature


TypeError raised
    if a field without a default value follows a field with a default value
    true whether occurs
        in a single class
        result of class inheritance

