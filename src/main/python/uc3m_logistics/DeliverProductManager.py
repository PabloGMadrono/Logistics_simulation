from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.order_request import OrderRequest
import re
from uc3m_logistics.storage.orders_json_store import OrderStore
from freezegun import freeze_time
from uc3m_logistics.storage.shipments_json_store import ShipmentStore
from datetime import datetime


class DeliverProductManager:

    def __init__(self, tracking_code):
        self.__tracking_code = tracking_code
        shipment = ShipmentStore()
        shipment.file_read()
        self.__data_list = shipment._data_list

    def validate_tracking_code(self):
        """Method for validating sha256 values"""
        myregex = re.compile(r"[0-9a-fA-F]{64}$")
        res = myregex.fullmatch(self.__tracking_code)
        if not res:
            raise OrderManagementException("tracking_code format is not valid")

    def check_date(self):
        """Method for checking the date"""
        found = False
        for item in self.__data_list:
            if item["_OrderShipping__tracking_code"] == self.__tracking_code:
                found = True
                del_timestamp = item["_OrderShipping__delivery_day"]
        if not found:
            raise OrderManagementException("tracking_code is not found")
        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(del_timestamp).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")