"""Contains the class OrderShipping"""
from datetime import datetime
import hashlib
from .attributes.product_id_validation import ProductId
from.attributes.email_validation import DeliveryEmail
from.attributes.order_id_validation import OrderID

#pylint: disable=too-many-instance-attributes
class OrderShipping():
    """Class representing the shipping of an order"""

    def __init__(self, product_id, order_id, delivery_email, order_type):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__product_id = ProductId(product_id).value
        self.__order_id = OrderID(order_id).value
        self.__delivery_email = DeliveryEmail(delivery_email).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        if order_type == "Regular":
            delivery_days = 7
        else:
            delivery_days = 1
        #timestamp is represneted in seconds.microseconds
        #__delivery_day must be expressed in senconds to be added to the timestap
        self.__delivery_day = self.__issued_at + (delivery_days * 24 * 60 * 60)
        self.__tracking_code = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string( self ):
        """Composes the string to be used for generating the tracking_code"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",order_id:" + \
               self.__order_id + ",issuedate:" + str(self.__issued_at) + \
               ",deliveryday:" + str(self.__delivery_day) + "}"

    @property
    def product_id( self ):
        """Property that represents the product_id of the order"""
        return self.__product_id

    @product_id.setter
    def product_id( self, product_id ):
        self.__product_id = ProductId(product_id).value

    @property
    def order_id( self ):
        """Property that represents the order_id"""
        return self.__order_id

    @order_id.setter
    def order_id(self, order_id):
        self.__order_id = OrderID(order_id).value

    @property
    def delivery_email(self):
        """Property that represents the email of the client"""
        return self.__delivery_email

    @delivery_email.setter
    def delivery_email(self, delivery_email):
        self.__delivery_email = DeliveryEmail(delivery_email).value

    @property
    def tracking_code( self ):
        """returns the tracking code"""
        return self.__tracking_code

    @property
    def issued_at( self ):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at( self, value ):
        self.__issued_at = value

    @property
    def delivery_day( self ):
        """Returns the delivery day for the order"""
        return self.__delivery_day
