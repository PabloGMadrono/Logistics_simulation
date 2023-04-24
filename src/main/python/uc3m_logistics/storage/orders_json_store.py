"""Method for order store in JSON"""
from .json_store import JSONStore
from ..order_manager_config import JSON_FILES_PATH
from ..order_management_exception import OrderManagementException

class OrderStore(JSONStore):
    """Class for order Store"""
    _file_store = JSON_FILES_PATH + "orders_store.json"

    def add(self, item):
        """Add method for order store json"""
        found = self.find("_OrderRequest__order_id", item.order_id)
        if found:
            raise OrderManagementException("order_id is already registered in orders_store")
        super().add(item)
