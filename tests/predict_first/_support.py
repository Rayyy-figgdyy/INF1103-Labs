"""Shared setup so section scripts can be run directly from any directory."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from Order import Order
from ProductFactory import ProductFactory
from Supplier import Supplier


def supplier():
    return Supplier("S001", "Test Supplier", "test@example.com")


def order_with_total_250(discount=None):
    product = ProductFactory.create("physical", "P001", "Test Product", 50, 10, supplier())
    order = Order("O001", discount)
    order.add_order_line(product, 3)
    order.add_order_line(product, 2)
    return order
