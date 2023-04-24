"""Module for Shipment delivering storage"""
from .json_store import JSONStore
from ..order_manager_config import JSON_FILES_PATH
from ..order_management_exception import OrderManagementException


class ShipmentDeliver(JSONStore):
    """Class for shipment delivering storage"""
    _file_store = JSON_FILES_PATH + "shipments_delivered.json"

    def add(self, item):
        """add method"""
        found = self.find("_OrderRequest__order_id", item.order_id)
        if found:
            raise OrderManagementException("order_id is already registered in orders_store")
        super().add(item)
