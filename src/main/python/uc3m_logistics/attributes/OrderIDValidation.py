from .attributes import Attribute
from ..order_management_exception import OrderManagementException
import re

class OrderID(Attribute):
    def __init__(self, attr_value):
        self._error_message = "order id is not valid"
        self._validation_pattern = r"[0-9a-fA-F]{32}$"
        self._attr_value = self._validate(attr_value)



    """def _validate(self, attr_value):

        try:
            myregex = re.compile(self._validation_pattern)
            result = myregex.fullmatch(attr_value)
            if not result:
                type = type[0].lower() + type[1:]
                for letter in range(len(type)):
                    if type[letter].isupper():
                        type = type[0: letter] + " " + type[letter:].lower()
                        break
                raise OrderManagementException(type + " is not valid")
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex
        return attr_value"""
