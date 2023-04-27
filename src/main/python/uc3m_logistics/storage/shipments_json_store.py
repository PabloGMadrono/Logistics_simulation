""" Method for Shipment store"""
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.storage.json_store import JSONStore


# pylint: disable=too-few-public-methods
class ShipmentStore:
    """Singleton for ShipmentStore"""
    class SingletonShipmentStore(JSONStore):
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
            ShipmentStore.instance = ShipmentStore.SingletonShipmentStore()
        return ShipmentStore.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)