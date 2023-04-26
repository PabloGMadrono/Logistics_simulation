"""JSON store module"""
import json
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.order_manager_config import JSON_FILES_PATH


class JSONStore:
    # pylint: disable=too-few-public-methods
    """Class for JSON store"""
    _file_store = " "
    _data_list = []

    def write_file(self):
        """Method to write in a file"""
        try:
            with open(self._file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex

    def file_open(self):
        """New method to get order_list and return empty order_list if not found file"""
        try:
            with open(self._file_store, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def file_read(self):
        """Difference with file_open is file not found error"""
        try:
            with open(self._file_store, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise OrderManagementException(
                self._file_store[len(JSON_FILES_PATH):-5]
                + " " + "not found") from ex

    def find(self, key, value):
        """method for finding values"""
        self.file_open()
        for item in self._data_list:
            if item[key] == value:
                return item
        return None

    def add(self, item):
        """method for adding items"""
        found = self.find("_OrderRequest__order_id", item.order_id)
        if found:
            raise OrderManagementException("order_id is already registered in orders_store")
        self.file_open()
        self._data_list.append(item.__dict__)
        self.write_file()

    def store_orders(self):
        """Method for saving the orders store"""
        self.file_open()
        self.add(self._data_list)
