"""Module for order type validation"""
from .attributes import Attribute


class OrderType(Attribute):
    """Class for order type validation"""
    # pylint: disable=too-few-public-methods
    def __init__(self, attr_value):
        """init method"""
        self._error_message = "order_type is not valid"
        self._validation_pattern = r"(Regular|Premium)"
        self._attr_value = self._validate(attr_value)
