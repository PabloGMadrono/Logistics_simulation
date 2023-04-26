
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.order_request import OrderRequest
import re
from uc3m_logistics.storage.orders_json_store import OrderStore
from freezegun import freeze_time
from datetime import datetime
import json
from .order_manager_config import JSON_FILES_PATH

class InputFileShipment:

    def __init__(self, input_file):
        self.__input_file = input_file

    def check_label(self, list):
        try:
            order_id = list["OrderID"]
            email = list["ContactEmail"]
        except KeyError as ex:
            raise OrderManagementException("Bad label")
        return order_id, email

    def file_read(self, input):
        """Difference with file_open is file not found error"""
        try:
            with open(input, "r", encoding="utf-8", newline="") as file:
                list = json.load(file)
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise OrderManagementException(
                input[len(JSON_FILES_PATH):-5]
                + " " + "not found") from ex
        return list

    def regex_check(self, order_id, email):
        myregex = re.compile(r"[0-9a-fA-F]{32}$")
        order_id_check = myregex.fullmatch(order_id)
        myregex = re.compile(r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$')
        email_check = myregex.fullmatch(email)
        if not order_id_check:
            raise OrderManagementException("order id is not valid")
        if not email_check:
            raise OrderManagementException("contact email is not valid")

    def create_object(self):
        mylist = self.file_read(self.__input_file)
        order_id, email = self.check_label(mylist)
        self.regex_check(order_id, email)
        item = self.find("_OrderRequest__order_id", order_id)
        if item:
            # retrieve the orders data
            product_id = item["_OrderRequest__product_id"]
            address = item["_OrderRequest__delivery_address"]
            reg_type = item["_OrderRequest__order_type"]
            phone = item["_OrderRequest__phone_number"]
            order_timestamp = item["_OrderRequest__time_stamp"]
            zip_code = item["_OrderRequest__zip_code"]
            # set the time when the order was registered for checking the md5
            with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
                order = OrderRequest(product_id=product_id,
                                     delivery_address=address,
                                     order_type=reg_type,
                                     phone_number=phone,
                                     zip_code=zip_code)

            if order.order_id != order_id:
                raise OrderManagementException("Orders' data have been manipulated")
        else:
            raise OrderManagementException("order_id not found")
        return product_id, reg_type, order_id, email

    def find(self, key, value):
        """method for finding values"""
        lists = self.file_read(JSON_FILES_PATH + "orders_store.json")
        for item in lists:
            if item[key] == value:
                return item
        return None