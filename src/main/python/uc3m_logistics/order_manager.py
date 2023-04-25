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

from uc3m_logistics.InputShipment import InputFileShipment
from uc3m_logistics.DeliverProductManager import DeliverProductManager

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
        input_file = InputFileShipment(order._data_list)
        product_id, reg_type = input_file.create_object()

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
        deliver_manager = DeliverProductManager(tracking_code)
        deliver_manager.validate_tracking_code()
        deliver_manager.check_date()
        # check if this tracking_code is in shipments_store

        # first read the file



        # search this tracking_code
        shipment_delivers = ShipmentDeliver()
        shipment_delivers.file_open()
        # append the delivery info
        shipment_delivers._data_list.append(str(tracking_code))
        shipment_delivers._data_list.append(str(datetime.utcnow()))

        shipment_delivers.write_file()
        return True



