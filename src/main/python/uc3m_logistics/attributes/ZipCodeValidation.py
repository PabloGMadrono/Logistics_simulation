from.attributes import Attribute
from..order_management_exception import OrderManagementException

class ZipCode(Attribute):
    def __init__(self, attr_value):
        self._error_message = "zip_code format is not valid"
        self._validation_pattern = ""
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        if attr_value.isnumeric() and len(attr_value) == 5:
            if int(attr_value) > 52999 or int(attr_value) < 1000:
                raise OrderManagementException("zip_code is not valid")
        else:
            raise OrderManagementException("zip_code format is not valid")
        return attr_value
