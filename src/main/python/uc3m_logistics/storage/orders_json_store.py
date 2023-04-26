"""Method for order store in JSON"""
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.storage.json_store import JSONStore


class OrderStore:
    # pylint: disable=too-few-public-methods
    """Singleton for OrderStore"""
    class SingletonOrderStore(JSONStore):
        # pylint: disable=too-few-public-methods
        """Class for order Store"""
        def __init__(self):
            pass

        _file_store = JSON_FILES_PATH + "orders_store.json"

    instance = None

    def __new__(cls):
        if not OrderStore.instance:
            OrderStore.instance = OrderStore.SingletonOrderStore()
        return OrderStore.instance
