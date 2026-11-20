"""Predict: loading the sample CSV, then loading after it has been renamed."""
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _support import supplier
from Inventory import Inventory
from inventory_manager import load_products


SAMPLE = (
    "product_type,product_id,name,price,stock_quantity\n"
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "products.csv"
        path.write_text(SAMPLE, encoding="utf-8")
        inventory = Inventory()
        output = StringIO()
        with redirect_stdout(output):
            load_products(str(path), inventory, supplier())
        lines = output.getvalue().splitlines()
        assert len(inventory.to_dict()["products"]) == 3
        assert len(lines) == 4
        assert lines[0] == "Skipping row 4: Unknown product type: service"
        assert lines[1].startswith("Skipping row 5:") and "abc" in lines[1]
        assert lines[2:] == ["3 products loaded.", "Load attempt finished."]
        print("File exists: else and finally run; the per-row except handles two bad rows.")
        print(output.getvalue(), end="")

        path.rename(path.with_name("renamed_products.csv"))
        output = StringIO()
        missing_inventory = Inventory()
        with redirect_stdout(output):
            load_products(str(path), missing_inventory, supplier())
        assert output.getvalue().splitlines() == [
            f"Products file not found: {path}", "Load attempt finished."
        ]
        assert missing_inventory.to_dict()["products"] == []
        print("\nFile renamed: FileNotFoundError except and finally run; else is skipped.")
        print(output.getvalue(), end="")
        print("Only temporary files were used; your actual products.csv was not renamed.")


if __name__ == "__main__":
    main()
