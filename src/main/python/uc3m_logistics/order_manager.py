"""Module """
from uc3m_logistics.order_request import OrderRequest
from uc3m_logistics.order_shipping import OrderShipping
from uc3m_logistics.storage.orders_json_store import OrderStore
from uc3m_logistics.storage.shipments_json_store import ShipmentStore

from uc3m_logistics.input_shipment import InputFileShipment
from uc3m_logistics.deliver_product_manager import DeliverProductManager


class OrderManager:
    # pylint: disable=too-few-public-methods
    """Singleton for order manager"""
    class SingletonOrderManager:
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
            input_file = InputFileShipment(order_file)
            product_id, reg_type, order_id, email = input_file.create_object()
            shipments = OrderShipping(product_id=product_id,
                                      order_id=order_id,
                                      order_type=reg_type,
                                      delivery_email=email)
            shipment = ShipmentStore()
            shipment.add(shipments)
            return shipments.tracking_code

        def deliver_product(self, tracking_code):
            """Register the delivery of the product"""
            deliver_manager = DeliverProductManager(tracking_code)
            deliver_manager.validate_tracking_code()
            deliver_manager.check_date()
            deliver_manager.create_delivery()
            return True

    instance = None

    def __new__(cls):
        if not OrderManager.instance:
            OrderManager.instance = OrderManager.SingletonOrderManager()
        return OrderManager.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
