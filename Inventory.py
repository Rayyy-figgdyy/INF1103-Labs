from Product import Product

class Inventory:
    def __init__(self):
        self.__products: list[Product] = []
        self.__transactions: list[dict] = []

    def add_product(self, product, record_transaction=True) -> bool:
        if self.search_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        if record_transaction:
            self.__transactions.append({
                "type": "ADD",
                "product_id": product.product_id,
                "amount": product.stock,
            })
        return True

    def remove_product(self, product_id: str) -> bool:
        product = self.search_product(product_id)

        if product is None:
            return False

        self.__products.remove(product)
        return True

    def search_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def update_stock(self, product_id: str, quantity: int) -> bool:
        product = self.search_product(product_id)
        if product is None:
            return False
        change = product.update_stock(quantity)
        self.__transactions.append({
            "type": "UPDATE",
            "product_id": product_id,
            "amount": change,
        })
        return True

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()
                print(product.get_fulfilment_info())
                print("-" * 48)
        if not self.__products:
            print("-" * 48)

    def to_dict(self) -> dict:
        return {
            "products": [product.to_dict() for product in self.__products],
            "transactions": self.__transactions,
        }

    def load_transactions(self, transactions) -> None:
        self.__transactions = list(transactions)
