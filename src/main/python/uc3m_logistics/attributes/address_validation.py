"""Module for Address validation"""
from .attributes import Attribute


class Address(Attribute):
    """Class for address validation"""

    # pylint: disable=too-few-public-methods
    def __init__(self, attr_value):
        """init method"""
        self._error_message = "address is not valid"
        self._validation_pattern = r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$"
        self._attr_value = self._validate(attr_value)
