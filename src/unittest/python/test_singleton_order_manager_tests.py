"""Singleton tests"""
from unittest import TestCase
from uc3m_logistics import OrderManager


class SingletonTests(TestCase):
    """Unitest class for singleton testing"""
    def test_singleton_order_manager(self):
        """Testing singleton for order manager"""
        order_manager_1 = OrderManager()
        order_manager_2 = OrderManager()
        order_manager_3 = OrderManager()
        self.assertEqual(order_manager_1, order_manager_2)
        self.assertEqual(order_manager_2, order_manager_3)
        self.assertEqual(order_manager_1, order_manager_3)
