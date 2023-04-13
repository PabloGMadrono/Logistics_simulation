from ..order_management_exception import OrderManagementException
import re

class Attribute():
    #Important values must be empty
    def __init__(self):
        self._attr_value = ""
        self._error_message = ""
        self._validation_pattern = ""

    def _validate(self, attr_value):
        my_regex = re.compile(self._validation_pattern)
        res = my_regex.fullmatch(attr_value)
        if not res:
            raise OrderManagementException(self._error_message)
        return attr_value

    @property
    def value(self):
        return self._attr_value

    @value.setter
    def value(self, value):
        self._attr_value = self._validate(value)

    def __str__(self):
        return self._attr_value