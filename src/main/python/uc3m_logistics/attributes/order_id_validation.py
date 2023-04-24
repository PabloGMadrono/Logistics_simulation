"""Module for Order id validation"""
from .attributes import Attribute


class OrderID(Attribute):
    """Class for order id validation"""

    # pylint: disable=too-few-public-methods
    def __init__(self, attr_value):
        """init method"""
        self._error_message = "order id is not valid"
        self._validation_pattern = r"[0-9a-fA-F]{32}$"
        self._attr_value = self._validate(attr_value)
