from Product import Product
from Supplier import Supplier

class DigitalProduct(Product):
    """A digital product with a downloadable file size."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size = float(download_size)
        if self.__download_size < 0:
            raise ValueError("Download size cannot be negative.")

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size:.2f} MB")
        print("---Supplier Information---")
        self.supplier.display_information()

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally by download."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
