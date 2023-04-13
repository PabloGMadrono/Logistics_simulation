from .attributes import Attribute
from ..order_management_exception import OrderManagementException

class ProductId(Attribute):
    def __init__(self, attr_value):
        self._error_message = "Invalid EAN13 code string"
        self._validation_pattern = r"^[0-9]{13}$"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE EAN13
        # RETURN TRUE IF THE EAN13 IS RIGHT, OR FALSE IN OTHER CASE
        super()._validate(attr_value)
        checksum = 0
        code_read = -1
        res = False


        for i, digit in enumerate(reversed(attr_value)):
            try:
                current_digit = int(digit)
            except ValueError as v_e:
                raise OrderManagementException("Invalid EAN13 code string") from v_e
            if i == 0:
                code_read = current_digit
            else:
                checksum += (current_digit) * 3 if (i % 2 != 0) else current_digit
        control_digit = (10 - (checksum % 10)) % 10

        if (code_read != -1) and (code_read == control_digit):
            res = True
        else:
            raise OrderManagementException("Invalid EAN13 control digit")
        return attr_value
