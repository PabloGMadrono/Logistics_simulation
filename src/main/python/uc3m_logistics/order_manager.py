"""Module """
import datetime
import re
import json
from datetime import datetime
from freezegun import freeze_time
from .order_request import OrderRequest
from .order_management_exception import OrderManagementException
from .order_shipping import OrderShipping
from .order_manager_config import JSON_FILES_PATH
from .storage.orders_json_store import order_store
from.storage.shipments_json_store import shipment_store
from .storage.shipments_deliver_json_store import shipment_deliver
from .storage.JSONstore import JSONStore

class OrderManager:
    """Class for providing the methods for managing the orders process"""
    def __init__(self):
        pass

        # pylint: disable=too-many-arguments
    def register_order(self, product_id,
                        order_type,
                        address,
                        phone_number,
                        zip_code):
        """Register the orders into the order's file"""
        order = OrderRequest(product_id,
                              order_type,
                              address,
                              phone_number,
                              zip_code)

        orders = order_store()
        orders.add(order)

        return order.order_id

        # pylint: disable=too-many-locals
    def send_order(self, order_file):
        """Sends the order included in the input_file"""
        order = order_store()
        order._file_store = order_file
        order.file_read()

        # check all the information
        #self.regex_check(order_data, r"[0-9a-fA-F]{32}$", "OrderID")
        #self.regex_check(order_data, r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$', "ContactEmail")


        product_id, reg_type = self.validate_order_id(order._data_list)

        shipments = OrderShipping(product_id=product_id,
                                    order_id=order._data_list["OrderID"],
                                    order_type=reg_type,
                                    delivery_email=order._data_list["ContactEmail"])

        # save the OrderShipping in shipments_store.json

        shipment = shipment_store()
        shipment.add(shipments)

        return shipments.tracking_code

    def deliver_product(self, tracking_code):
        """Register the delivery of the product"""
        self.validate_tracking_code(tracking_code)
        # check if this tracking_code is in shipments_store

        # first read the file
        shipment = shipment_store()
        shipment.file_read()

        # search this tracking_code
        self.check_date(shipment._data_list, tracking_code)
        shipment_delivers = shipment_deliver()
        shipment_delivers.file_open()
        # append the delivery info
        shipment_delivers._data_list.append(str(tracking_code))
        shipment_delivers._data_list.append(str(datetime.utcnow()))

        shipment_delivers.write_file()
        return True


    def validate_tracking_code(self, tracking_code):
        """Method for validating sha256 values"""
        myregex = re.compile(r"[0-9a-fA-F]{64}$")
        res = myregex.fullmatch(tracking_code)
        if not res:
            raise OrderManagementException("tracking_code format is not valid")

    def check_date(self, data_list, tracking_code):
        found = False
        for item in data_list:
            if item["_OrderShipping__tracking_code"] == tracking_code:
                found = True
                del_timestamp = item["_OrderShipping__delivery_day"]
        if not found:
            raise OrderManagementException("tracking_code is not found")
        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(del_timestamp).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")




    def validate_order_id(self, order_data):
        try:
            myregex = re.compile(r"[0-9a-fA-F]{32}$")
            order_id_check = myregex.fullmatch(order_data["OrderID"])
            myregex = re.compile(r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$')
            email_check = myregex.fullmatch(order_data["ContactEmail"])
            if not order_id_check:
                raise OrderManagementException("order id is not valid")
            if not email_check:
                raise OrderManagementException("contact email is not valid")
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex

        order_json_store = order_store()
        item = order_json_store.find("_OrderRequest__order_id", order_data["OrderID"])

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

                if order.order_id != order_data["OrderID"]:
                    raise OrderManagementException("Orders' data have been manipulated")
        else:
            raise OrderManagementException("order_id not found")
        return product_id, reg_type



    """
        def store_orders(self, orders, file_store):
        """"""Method for saving the orders store""""""
        #first read the file
        order_list = self.file_open(file_store)

        self.data_list_append(order_list, orders)
        self.write_file(order_list, file_store)"""

    """
    def data_list_append(self, data_list, data):
        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == data.order_id:
                found = True
        if found is False:
            data_list.append(data.__dict__)
        else:
            raise OrderManagementException("order_id is already registered in orders_store")"""


    """    
        def file_open(self, path_store):
        #New method to get order_list and return empty order_list if not found file
        try:
            with open(path_store, "r", encoding="utf-8", newline="") as file:
                order_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            order_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return order_list"""

    """

    def write_file(self, data_list, file_store):
        #Method to write in a file
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex
    """








    """def regex_check(self, data, order_reg, type):
        try:
            myregex = re.compile(order_reg)
            result = myregex.fullmatch(data[type])

            if not result:
                type = type[0].lower() + type[1:]
                for letter in range(len(type)):
                    if type[letter].isupper():
                        type = type[0: letter] + " " + type[letter:].lower()
                        break

                raise OrderManagementException(type + " is not valid")
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex"""






    """def file_read(self, path_store):
        #Difference with file_open is file not found error
        try:
            with open(path_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise OrderManagementException(path_store[len(JSON_FILES_PATH):-5] + " " + "not found") from ex
        return data_list"""
