"""Module Attributes"""
import re

from ..order_management_exception import OrderManagementException

class Attribute():
    """General Class attributes"""
    def __init__(self):
        """Init method"""
        self._attr_value = ""
        self._error_message = ""
        self._validation_pattern = ""

    def _validate(self, attr_value):
        """General validation method"""
        try:
            my_regex = re.compile(self._validation_pattern)
            res = my_regex.fullmatch(attr_value)
            if not res:
                raise OrderManagementException(self._error_message)
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex

        return attr_value

    @property
    def value(self):
        """value property"""
        return self._attr_value

    @value.setter
    def value(self, value):
        """value setter"""
        self._attr_value = self._validate(value)

    def __str__(self):
        """str method"""
        return self._attr_value
