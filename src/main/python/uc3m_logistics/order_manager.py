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

class OrderManager:
    """Class for providing the methods for managing the orders process"""
    def __init__(self):
        pass

    @staticmethod
    def validate_ean13( ean13 ):
        """method for validating a ean13 code"""
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE EAN13
        # RETURN TRUE IF THE EAN13 IS RIGHT, OR FALSE IN OTHER CASE
        checksum = 0
        code_read = -1
        res = False
        regex_ean13 = re.compile("^[0-9]{13}$")
        valid_ean13_format = regex_ean13.fullmatch(ean13)
        if valid_ean13_format is None:
            raise OrderManagementException("Invalid EAN13 code string")

        for i, digit in enumerate(reversed(ean13)):
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
        return res

    @staticmethod
    def validate_tracking_code( t_c ):
        """Method for validating sha256 values"""
        myregex = re.compile(r"[0-9a-fA-F]{64}$")
        res = myregex.fullmatch(t_c)
        if not res:
            raise OrderManagementException("tracking_code format is not valid")

    @staticmethod
    def save_order_store(orders):
        """Medthod for saving the orders store"""
        order_store = JSON_FILES_PATH + "orders_store.json"
        #first read the file
        order_list = OrderManager.file_open(order_store)

        OrderManager.data_list_append(order_list, orders)
        OrderManager.write_file(order_list, order_store)
        return True

    @staticmethod
    def data_list_append(data_list, data):
        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == data.order_id:
                found = True
        if found is False:
            data_list.append(data.__dict__)
        else:
            raise OrderManagementException("order_id is already registered in orders_store")

    @staticmethod
    def file_open(path_store):
        #New method to get order_list and return empty order_list if not found file
        try:
            with open(path_store, "r", encoding="utf-8", newline="") as file:
                order_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            order_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return order_list

    #@staticmethod
    """def save_fast(data):
        """"""Method for saving the orders store""""""
        orders_store = JSON_FILES_PATH + "orders_store.json"
        with open(orders_store, "r+", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
            data_list.append(data.__dict__)
            file.seek(0)
            json.dump(data_list, file, indent=2)
            esto sobra creo"""

    @staticmethod
    def save_orders_shipped( shipment ):
        """Saves the shipping object into a file"""
        shipments_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        shipment_list = OrderManager.file_open(shipments_store_file)
        #append the shipments list
        shipment_list.append(shipment.__dict__)

        OrderManager.write_file(shipment_list, shipments_store_file)

    @staticmethod
    def write_file(data_list, file_store):
        #Method to write in a file
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex

    #pylint: disable=too-many-arguments
    def register_order( self, product_id,
                        order_type,
                        address,
                        phone_number,
                        zip_code ):
        """Register the orders into the order's file"""

        self.validate_order_type(order_type)

        self.validate_address(address)

        self.validate_phone_number(phone_number)
        #Hemos extraido el metodo para simplificar el codigo

        if self.validate_ean13(product_id):
            my_order = OrderRequest(product_id,
                                    order_type,
                                    address,
                                    phone_number,
                                    zip_code)

        self.save_order_store(my_order)

        return my_order.order_id



    def validate_order_type(self, order_type):
        myregex = re.compile(r"(Regular|Premium)")
        res = myregex.fullmatch(order_type)
        if not res:
            raise OrderManagementException("order_type is not valid")

    def validate_address(self, address):
        myregex = re.compile(r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$")
        res = myregex.fullmatch(address)
        if not res:
            raise OrderManagementException("address is not valid")

    def validate_phone_number(self, phone_number):
        myregex = re.compile(r"^(\+)[0-9]{11}")
        res = myregex.fullmatch(phone_number)
        if not res:
            raise OrderManagementException("phone number is not valid")

    #pylint: disable=too-many-locals
    def send_order(self, order_file):
        """Sends the order included in the input_file"""
        order_data = OrderManager.file_read(order_file)

        #check all the information
        OrderManager.regex_check(order_data, r"[0-9a-fA-F]{32}$", "OrderID")
        OrderManager.regex_check(order_data, r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$',"ContactEmail")

        file_store = JSON_FILES_PATH + "orders_store.json"

        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == order_data["OrderID"]:
                found = True
                #retrieve the orders data
                proid = item["_OrderRequest__product_id"]
                address = item["_OrderRequest__delivery_address"]
                reg_type = item["_OrderRequest__order_type"]
                phone = item["_OrderRequest__phone_number"]
                order_timestamp = item["_OrderRequest__time_stamp"]
                zip_code = item["_OrderRequest__zip_code"]
                #set the time when the order was registered for checking the md5
                with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
                    order = OrderRequest(product_id=proid,
                                         delivery_address=address,
                                         order_type=reg_type,
                                         phone_number=phone,
                                         zip_code=zip_code)

                print(order_data["OrderID"])
                if order.order_id != order_data["OrderID"]:
                    raise OrderManagementException("Orders' data have been manipulated")

        if not found:
            raise OrderManagementException("order_id not found")

        my_sign= OrderShipping(product_id=proid,
                               order_id=order_data["OrderID"],
                               order_type=reg_type,
                               delivery_email=order_data["ContactEmail"])

        #save the OrderShipping in shipments_store.json

        self.save_orders_shipped(my_sign)

        return my_sign.tracking_code
    @staticmethod
    def regex_check(data, order_reg, type):
        try:
            myregex = re.compile(order_reg)
            res = myregex.fullmatch(data[type])

            if not res:
                type = type[0].lower() + type[1:]
                for letter in range(len(type)):
                    if type[letter].isupper():
                        type = type[0: letter] + " " + type[letter:].lower()
                        break

                raise OrderManagementException(type + " is not valid")
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex

    def deliver_product( self, tracking_code ):
        """Register the delivery of the product"""
        self.validate_tracking_code(tracking_code)

        #check if this tracking_code is in shipments_store
        shimpents_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        shipments_list = self.file_read(shimpents_store_file)
        #search this tracking_code
        found = False
        for item in shipments_list:
            if item["_OrderShipping__tracking_code"] == tracking_code:
                found = True
                del_timestamp = item["_OrderShipping__delivery_day"]
        if not found:
            raise OrderManagementException("tracking_code is not found")

        today= datetime.today().date()
        delivery_date= datetime.fromtimestamp(del_timestamp).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")

        shipments_file = JSON_FILES_PATH + "shipments_delivered.json"

        shipments_list = OrderManager.file_open(shipments_file)

            # append the delivery info
        shipments_list.append(str(tracking_code))
        shipments_list.append(str(datetime.utcnow()))
        OrderManager.write_file(shipments_list, shipments_file)
        return True
    @staticmethod
    def file_read(path_store):
        #Difference with file_open is file not found error
        try:
            with open(path_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise OrderManagementException(path_store[len(JSON_FILES_PATH):-5] + " " + "not found") from ex
        return data_list
