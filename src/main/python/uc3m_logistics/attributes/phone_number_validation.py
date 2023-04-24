"""Module for phone number validation"""
from .attributes import Attribute


class PhoneNumber(Attribute):
    """Class for phone number validation"""

    # pylint: disable=too-few-public-methods
    def __init__(self, attr_value):
        """init method"""
        self._error_message = "phone number is not valid"
        self._validation_pattern = r"^(\+)[0-9]{11}"
        self._attr_value = self._validate(attr_value)
