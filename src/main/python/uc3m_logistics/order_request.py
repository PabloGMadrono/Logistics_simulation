"""MODULE: order_request. Contains the order request class"""
import hashlib
import json
from datetime import datetime
from uc3m_logistics.attributes.phone_number_validation import PhoneNumber
from uc3m_logistics.attributes.product_id_validation import ProductId
from uc3m_logistics.attributes.address_validation import Address
from uc3m_logistics.attributes.order_type_validation import OrderType
from uc3m_logistics.attributes.zip_code_validation import ZipCode


class OrderRequest:
    """Class representing the register of the order in the system"""
    #pylint: disable=too-many-arguments
    def __init__( self, product_id, order_type,
                  delivery_address, phone_number, zip_code):
        self.__product_id = ProductId(product_id).value
        self.__delivery_address = Address(delivery_address).value
        self.__order_type = OrderType(order_type).value
        self.__phone_number = PhoneNumber(phone_number).value
        justnow = datetime.utcnow()
        self.__zip_code = ZipCode(zip_code).value
        self.__time_stamp = datetime.timestamp(justnow)
        self.__order_id = hashlib.md5(self.__str__().encode()).hexdigest()

    def __str__(self):
        return "OrderRequest:" + json.dumps(self.__dict__)

    @property
    def delivery_address(self):
        """Property representing the address where the product
        must be delivered"""
        return self.__delivery_address

    @delivery_address.setter
    def delivery_address(self, delivery_address):
        self.__delivery_address = Address(delivery_address).value

    @property
    def order_type( self ):
        """Property representing the type of order: REGULAR or PREMIUM"""
        return self.__order_type

    @order_type.setter
    def order_type( self, order_type):
        self.__order_type = OrderType(order_type).value

    @property
    def phone_number(self):
        """Property representing the client's phone number"""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = PhoneNumber(value).value

    @property
    def product_id(self):
        """Property representing the products  EAN13 code"""
        return self.__product_id

    @product_id.setter
    def product_id(self, product_id):
        self.__product_id = ProductId(product_id).value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def order_id( self ):
        """Returns the md5 signature"""
        return self.__order_id

    @property
    def zip_code(self):
        """Returns the order's zip_code"""
        return self.__zip_code

    @zip_code.setter
    def zip_code(self, zip_code):
        self.__zip_code == ZipCode(zip_code).value
