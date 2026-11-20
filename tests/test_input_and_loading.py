import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import inventory_manager as manager
from Inventory import Inventory
from ProductFactory import ProductFactory
from Supplier import Supplier


HEADER = "product_type,product_id,name,price,stock_quantity\n"
SAMPLE = HEADER + (
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)


class InputAndLoadingTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "products.csv"
        self.inventory = Inventory()
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    def load_csv(self, contents):
        self.path.write_text(contents, encoding="utf-8")
        output = StringIO()
        with redirect_stdout(output):
            manager.load_products(str(self.path), self.inventory, self.supplier)
        return output.getvalue().splitlines()

    def test_input_retries_until_positive_number(self):
        output = StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "0", "12.50"]) as ask:
            with redirect_stdout(output):
                result = manager.get_positive_float("Price: ")
        self.assertEqual(result, 12.5)
        self.assertEqual(ask.call_count, 4)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
            "Please enter a number greater than zero.",
        ])

    def test_sample_loads_three_products_and_reports_bad_rows(self):
        with patch.object(manager.ProductFactory, "create", wraps=ProductFactory.create) as create:
            lines = self.load_csv(SAMPLE)
        self.assertEqual(create.call_count, 4)  # The nonnumeric price fails before creation.
        self.assertEqual(lines[0], "Skipping row 4: Unknown product type: service")
        self.assertIn("Skipping row 5:", lines[1])
        self.assertIn("abc", lines[1])
        self.assertEqual(lines[2:], ["3 products loaded.", "Load attempt finished."])
        ids = [product["id"] for product in self.inventory.to_dict()["products"]]
        self.assertEqual(ids, ["P001", "D001", "P003"])
        self.assertIs(self.inventory.search_product("P001").supplier, self.supplier)
        self.assertEqual(self.inventory.search_product("P001").weight, 0)
        self.assertEqual(self.inventory.search_product("D001").download_size, 0)

    def test_missing_file_is_handled(self):
        output = StringIO()
        with redirect_stdout(output):
            manager.load_products(str(self.path), self.inventory, self.supplier)
        self.assertEqual(output.getvalue().splitlines(), [
            f"Products file not found: {self.path}", "Load attempt finished."
        ])
        self.assertEqual(self.inventory.to_dict()["products"], [])

    def test_duplicate_ids_are_not_counted_as_loaded(self):
        self.load_csv(HEADER + "physical,P001,Lamp,25,10\n")
        lines = self.load_csv(HEADER + "physical,P001,Replacement,30,5\n")
        self.assertEqual(lines, [
            "Skipping row 2: Product ID already exists.",
            "0 products loaded.", "Load attempt finished."
        ])
        self.assertEqual(self.inventory.search_product("P001").name, "Lamp")

    def test_invalid_rows_do_not_prevent_later_valid_rows_loading(self):
        lines = self.load_csv(HEADER + (
            "physical,missing_columns\n"
            "physical,P001,Free Lamp,0,10\n"
            "physical,P002,Lamp,25,-1\n"
            "digital,D001,Editor,49.90,abc\n"
            "physical,P003,Stand,39.50,7\n"
        ))
        self.assertEqual(len([line for line in lines if line.startswith("Skipping row")]), 4)
        self.assertEqual(lines[-2:], ["1 products loaded.", "Load attempt finished."])
        self.assertIsNotNone(self.inventory.search_product("P003"))

    def test_empty_and_header_only_files(self):
        for contents in ["", HEADER]:
            with self.subTest(contents=contents):
                self.assertEqual(self.load_csv(contents), [
                    "0 products loaded.", "Load attempt finished."
                ])


if __name__ == "__main__":
    unittest.main()
