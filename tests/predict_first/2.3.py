"""Predict: bulk discount, then switching the same order to 10% off."""
from _support import order_with_total_250
from BulkDiscount import BulkDiscount
from PercentageDiscount import PercentageDiscount


def main():
    order = order_with_total_250(BulkDiscount(200, 20))
    bulk_total = order.calculate_total()
    assert bulk_total == 230
    print(f"BulkDiscount(200, 20): {bulk_total:.2f}")
    order.set_discount(PercentageDiscount(10))
    percentage_total = order.calculate_total()
    assert percentage_total == 225
    print(f"After set_discount(PercentageDiscount(10)): {percentage_total:.2f}")


if __name__ == "__main__":
    main()
