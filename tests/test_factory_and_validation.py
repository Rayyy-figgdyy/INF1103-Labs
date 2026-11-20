import unittest

from DigitalProduct import DigitalProduct
from Order import Order
from OrderLine import OrderLine
from PhysicalProduct import PhysicalProduct
from ProductFactory import ProductFactory
from Supplier import Supplier


class FactoryAndValidationTests(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    def create_product(self, kind="physical", price=25, stock=10, **details):
        return ProductFactory.create(
            kind, "P001", "Test Product", price, stock, self.supplier, **details
        )

    def test_factory_creates_physical_product(self):
        product = self.create_product(weight=1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.product_id, "P001")
        self.assertEqual(product.price, 25)
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.weight, 1.5)
        self.assertIs(product.supplier, self.supplier)

    def test_factory_creates_digital_product(self):
        product = self.create_product("digital", download_size=250)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.download_size, 250)
        self.assertIs(product.supplier, self.supplier)

    def test_factory_rejects_unknown_type(self):
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            self.create_product("service")

    def test_both_product_types_reject_nonpositive_prices(self):
        for kind in ["physical", "digital"]:
            for price in [0, -1]:
                with self.subTest(kind=kind, price=price):
                    with self.assertRaisesRegex(ValueError, "Price must be greater than zero"):
                        self.create_product(kind, price=price)

    def test_both_product_types_reject_negative_stock(self):
        for kind in ["physical", "digital"]:
            with self.subTest(kind=kind):
                with self.assertRaisesRegex(ValueError, "Stock cannot be negative"):
                    self.create_product(kind, stock=-1)

    def test_positive_price_and_zero_stock_are_valid(self):
        for kind in ["physical", "digital"]:
            with self.subTest(kind=kind):
                product = self.create_product(kind, price=0.01, stock=0)
                self.assertEqual(product.price, 0.01)
                self.assertEqual(product.stock, 0)

    def test_failed_stock_update_preserves_existing_stock(self):
        product = self.create_product()
        with self.assertRaisesRegex(ValueError, "Stock cannot be negative"):
            product.update_stock(-1)
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.update_stock(0), -10)
        self.assertEqual(product.stock, 0)

    def test_order_line_rejects_nonpositive_quantities(self):
        product = self.create_product()
        for quantity in [0, -1]:
            with self.subTest(quantity=quantity):
                with self.assertRaisesRegex(ValueError, "Quantity must be greater than zero"):
                    OrderLine(product, quantity)

    def test_order_line_calculates_subtotal(self):
        self.assertEqual(OrderLine(self.create_product(), 3).calculate_subtotal(), 75)

    def test_invalid_line_is_not_added_to_order(self):
        order = Order("O001")
        with self.assertRaises(ValueError):
            order.add_order_line(self.create_product(), 0)
        self.assertEqual(order.order_lines, ())


if __name__ == "__main__":
    unittest.main()
