"""Singleton tests"""
from unittest import TestCase
from uc3m_logistics import OrderManager
from uc3m_logistics.storage.shipments_json_store import ShipmentStore
from uc3m_logistics.storage.orders_json_store import OrderStore
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.input_shipment import InputFileShipment


class SingletonTests(TestCase):
    """Unitest class for singleton testing"""
    def test_singleton_(self):
        #Testing singleton for order manager
        order_manager_1 = OrderManager()
        order_manager_2 = OrderManager()
        order_manager_3 = OrderManager()
        self.assertEqual(order_manager_1, order_manager_2)
        self.assertEqual(order_manager_2, order_manager_3)
        self.assertEqual(order_manager_1, order_manager_3)
        #Testing singleton for shipment_store
        shipment_store_1 = ShipmentStore()
        shipment_store_2 = ShipmentStore()
        shipment_store_3 = ShipmentStore()
        self.assertEqual(shipment_store_1, shipment_store_2)
        self.assertEqual(shipment_store_1,shipment_store_3)
        self.assertEqual(shipment_store_2,shipment_store_3)
        #Testing singleton for order_Store
        order_store_1 = OrderStore()
        order_store_2 = OrderStore()
        order_store_3 = OrderStore()
        self.assertEqual(order_store_1,order_store_2)
        self.assertEqual(order_store_2, order_store_3)
        self.assertEqual(order_store_1, order_store_3)

    def test_no_singleton(self):
        """We now test two different objects without the singleton desing pattern to
        see they are different"""

        file_shipments_store = JSON_FILES_PATH + "shipments_store.json"
        input_shipment_1 = InputFileShipment(file_shipments_store)
        input_shipment_2 = InputFileShipment(file_shipments_store)
        self.assertNotEqual(input_shipment_1, input_shipment_2)
