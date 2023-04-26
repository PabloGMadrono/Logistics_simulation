""" Method for Shipment store"""
from .json_store import JSONStore
from ..order_manager_config import JSON_FILES_PATH
from ..order_management_exception import OrderManagementException

class ShipmentStore(JSONStore):
    class __ShipmentStore(JSONStore):

        # pylint: disable=too-few-public-methods
        """Class for shipment store"""
        def __init__(self):
            pass
        _file_store = JSON_FILES_PATH + "shipments_store.json"

        def add(self, item):
            """method for adding to Shipment sotorage"""
            found = self.find("_OrderRequest__order_id", item.order_id)
            if found:
                raise OrderManagementException("order_id is already registered in orders_store")
            super().add(item)

    instance = None

    def __new__(cls):
        if not ShipmentStore.instance:
            ShipmentStore.instance = ShipmentStore.__ShipmentStore()
        return ShipmentStore.instance
