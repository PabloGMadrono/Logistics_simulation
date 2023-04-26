from unittest import TestCase
import os
import json
import hashlib
from freezegun import freeze_time
from uc3m_logistics import OrderManager
from uc3m_logistics import OrderManagementException
from uc3m_logistics import JSON_FILES_PATH
from uc3m_logistics import JSON_FILES_RF2_PATH


class SingletonTests(TestCase):

    def test_singleton_order_manager(self):
        order_manager_1 = OrderManager()
        order_manager_2 = OrderManager()
        order_manager_3 = OrderManager()
        self.assertEqual(order_manager_1, order_manager_2)
        self.assertEqual(order_manager_2, order_manager_3)
        self.assertEqual(order_manager_1, order_manager_3)
