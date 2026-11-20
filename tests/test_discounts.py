import unittest

from BulkDiscount import BulkDiscount
from DiscountStrategy import DiscountStrategy
from NoDiscount import NoDiscount
from Order import Order
from PercentageDiscount import PercentageDiscount
from ProductFactory import ProductFactory
from StudentDiscount import StudentDiscount
from Supplier import Supplier


class DiscountTests(unittest.TestCase):
    def setUp(self):
        supplier = Supplier("S001", "Test Supplier", "test@example.com")
        self.product = ProductFactory.create(
            "physical", "P001", "Test Product", 50, 10, supplier
        )

    def test_abstract_strategy_cannot_be_created(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_no_discount(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)

    def test_bulk_discount_threshold(self):
        strategy = BulkDiscount(200, 20)
        for total, expected in [(199, 199), (200, 180), (250, 230)]:
            with self.subTest(total=total):
                self.assertEqual(strategy.apply(total), expected)

    def test_student_discount(self):
        self.assertAlmostEqual(StudentDiscount().apply(250), 237.50)

    def test_order_defaults_to_no_discount(self):
        order = Order("O001")
        order.add_order_line(self.product, 5)
        self.assertEqual(order.calculate_total(), 250)

    def test_empty_order_total(self):
        self.assertEqual(Order("O001").calculate_total(), 0)

    def test_discount_uses_combined_order_lines(self):
        order = Order("O001", BulkDiscount(200, 20))
        order.add_order_line(self.product, 3)
        order.add_order_line(self.product, 2)
        self.assertEqual(order.calculate_total(), 230)

    def test_switching_strategy_does_not_stack_discounts(self):
        order = Order("O001", BulkDiscount(200, 20))
        order.add_order_line(self.product, 5)
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)
        order.set_discount(NoDiscount())
        self.assertEqual(order.calculate_total(), 250)

    def test_order_accepts_new_strategy_without_changes(self):
        class FixedDiscount(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total - 7

        order = Order("O001", FixedDiscount())
        order.add_order_line(self.product, 5)
        self.assertEqual(order.calculate_total(), 243)


if __name__ == "__main__":
    unittest.main()
