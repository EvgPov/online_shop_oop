class Product:
    def __init__(self, name: str, price: float, quantity: int, product_id: str):
        self.name = str(name).strip()
        self._price = float(price)
        self._quantity = int(quantity)
        self.product_id = str(product_id).strip()

    def __str__(self) -> str:
        return  f"Наименование: {self.name}, Цена: {self.price}, Количество: {self.quantity}, ID: {self.product_id}"

    # геттер и сеттер для price
    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float) -> float:
        if new_price <= 0:
            raise ValueError("Цена должна быть прожительной")
        self._price = float(new_price)

    # геттер и сеттер для quantity
    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, new_quantity: int) -> int:
        if new_quantity < 0:
            raise ValueError("Количество дожно быть больше или равно нулю")
        self._quantity = float(new_quantity)

    def is_available(self, needed_quantity: int) -> bool:
        return self._quantity >= needed_quantity
# DigitalProduct
class DigitalProduct(Product):
    def __init__(self, name: str, price: float, product_id: str,
                 file_size: float, download_link: str):
        super().__init__(
            name=name,
            price=price,
            quantity=999_999_999, # очень большое число
            product_id=product_id
        )
        self.file_size = float(file_size)
        self.download_link = str(download_link).strip()

    def  __str__(self):
        return f"[ЦИФРОВОЙ] {self.name}, Цена: {self.price} руб., Размер(МБ): {self.file_size:}, ID: {self.product_id}"

    # цифровой товар всегда доступен, если количество не задано
    def  is_available(self, needed_quantity: int) -> bool:
        if needed_quantity is None:
            return True
        return self.quantity >= needed_quantity
# DiscountedProduct
class DiscountedProduct(Product):
    def __init__(self, name: str, price: float,
                 quantity: int, product_id: str,
                 discount_percent: float = 0.0):
        super().__init__(name, price,  quantity, product_id)
        self.discount_percent = discount_percent

    @property
    def price(self) -> float:
        discounted_price = self.price * (1 - self.discount_percent / 100)
        return max(0.0, discounted_price)
