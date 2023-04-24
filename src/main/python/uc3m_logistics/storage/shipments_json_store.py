""" Method for Shipment store"""
from .json_store import JSONStore
from ..order_manager_config import JSON_FILES_PATH
from ..order_management_exception import OrderManagementException


class ShipmentStore(JSONStore):
    # pylint: disable=too-few-public-methods
    """Class for shipment store"""
    _file_store = JSON_FILES_PATH + "shipments_store.json"

    def add(self, item):
        """method for adding to Shipment sotorage"""
        found = self.find("_OrderRequest__order_id", item.order_id)
        if found:
            raise OrderManagementException("order_id is already registered in orders_store")
        super().add(item)
