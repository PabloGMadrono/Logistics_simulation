"""Module for Product id validation"""
from .attributes import Attribute
from ..order_management_exception import OrderManagementException


class ProductId(Attribute):
    """Class for Product id validation"""
    # pylint: disable=too-few-public-methods
    def __init__(self, attr_value):
        """init method"""
        self._error_message = "Invalid EAN13 code string"
        self._validation_pattern = r"^[0-9]{13}$"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        """New validate method for product id"""
        super()._validate(attr_value)
        checksum = 0
        code_read = -1

        for index, digit in enumerate(reversed(attr_value)):
            try:
                current_digit = int(digit)
            except ValueError as value_error:
                raise OrderManagementException("Invalid EAN13 code string") from value_error
            if index == 0:
                code_read = current_digit
            else:
                checksum += current_digit * 3 if (index % 2 != 0) else current_digit
        control_digit = (10 - (checksum % 10)) % 10
        if not ((code_read != -1) and (code_read == control_digit)):
            raise OrderManagementException("Invalid EAN13 control digit")
        return attr_value
