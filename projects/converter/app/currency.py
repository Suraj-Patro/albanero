from enum import Enum


class Currency(Enum):
    PLN = "PLN"
    CZK = "CZK"
    DKK = "DKK"
    EUR = "EUR"
    GBP = "GBP"
    NOK = "NOK"
    USD = "USD"
    ZAR = "ZAR"

    @classmethod
    def is_member(cls, value: str) -> bool:
        """TODO: Part 1"""
        # check = False
        # for item in list(Currency):
        #     if item.value == value:
        #         check = True
        #         break
        # return check
        try:
            # Currency(value)   # because values can be redundant but keys cannot
            Currency[value]     # but value not used as its not used in cash.py
            return True
        # except:
        except KeyError:
            return False
