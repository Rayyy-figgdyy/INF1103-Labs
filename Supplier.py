class Supplier():
    """Abstract base class for all inventory products."""

    def __init__(self, supplier_id, name, contact_email):
        self.__supplier_id = supplier_id
        self.__name = name
        self.__contact_email = contact_email

    @property
    def supplier_id(self):
        return self.__supplier_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__contact_email 

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Name: {self.__name}")
        print(f"Contact Email: {self.__contact_email}")