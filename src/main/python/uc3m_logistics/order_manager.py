"""Module """
import re
from datetime import datetime

from freezegun import freeze_time

from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.order_request import OrderRequest
from uc3m_logistics.order_shipping import OrderShipping
from uc3m_logistics.storage.orders_json_store import OrderStore
from uc3m_logistics.storage.shipments_deliver_json_store import ShipmentDeliver
from uc3m_logistics.storage.shipments_json_store import ShipmentStore


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

        orders = OrderStore()
        orders.add(order)

        return order.order_id

        # pylint: disable=too-many-locals
        # pylint: disable=protected-access
    def send_order(self, order_file):
        """Sends the order included in the input_file"""
        order = OrderStore()
        order._file_store = order_file
        order.file_read()



        product_id, reg_type = self.validate_order_id(order._data_list)

        shipments = OrderShipping(product_id=product_id,
                                    order_id=order._data_list["OrderID"],
                                    order_type=reg_type,
                                    delivery_email=order._data_list["ContactEmail"])

        # save the OrderShipping in shipments_store.json

        shipment = ShipmentStore()
        shipment.add(shipments)

        return shipments.tracking_code

    def deliver_product(self, tracking_code):
        """Register the delivery of the product"""
        self.validate_tracking_code(tracking_code)
        # check if this tracking_code is in shipments_store

        # first read the file
        shipment = ShipmentStore()
        shipment.file_read()

        # search this tracking_code
        self.check_date(shipment._data_list, tracking_code)
        shipment_delivers = ShipmentDeliver()
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
        """Method for checking the date"""
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
        """Validate order id"""
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

        order_json_store = OrderStore()
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
