class Product:
    def __init__(self, name: str, price: float, quantity: int, product_id: str):
        self.__name = str(name).strip()
        self.__price = float(price)
        self.__quantity = int(quantity)
        self.product_id = str(product_id).strip()

    def __str__(self) -> str:
        # return  f"Наименование: {self.__name}, Цена: {self.__price}, Количество: {self.__quantity}, ID: {self.product_id}"
        return f"{self.__name} ({self.product_id}): {int(self.__price)} руб., в наличии: {self.__quantity}"

    # геттер для name
    @property
    def name(self) -> str:
        return self.__name

    # геттер и сеттер для price
    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> float:
        if new_price <= 0:
            raise ValueError("Цена должна быть прожительной")
        self.__price = float(new_price)

    # геттер и сеттер для quantity
    @property
    def quantity(self) -> int:
        return self.__quantity

    @quantity.setter
    def quantity(self, new_quantity: int) -> int:
        if new_quantity < 0:
            raise ValueError("Количество дожно быть больше или равно нулю")
        self.__quantity = float(new_quantity)

    def is_available(self, needed_quantity: int) -> bool:
        return self.__quantity >= needed_quantity

# DigitalProduct
class DigitalProduct(Product):
    def __init__(self, __name: str, __price: float, __quantity: int, product_id: str,
                 file_size: float, download_link: str):
        super().__init__(__name, __price,  1000, product_id)
        self.file_size = float(file_size)
        self.download_link = str(download_link).strip()

    def  __str__(self):
        return (f"{self.name} ({self.product_id}): {int(self.price)} руб., в наличии: {self.quantity}, "
                f"формат: цифровой, размер: {int(self.file_size)} МБ")

    # цифровой товар всегда доступен, если количество не задано
    def  is_available(self, needed_quantity: int) -> bool:
        if needed_quantity is None:
            return True
        return self.quantity >= needed_quantity

# DiscountedProduct
class DiscountedProduct(Product):
    def __init__(self, __name: str, __price: float,
                 __quantity: int, product_id: str,
                 discount_percent: float = 0.0):
        super().__init__(__name, __price, __quantity, product_id)
        self.__discount_percent = discount_percent

    #геттер и сеттер для discount_percent
    @property
    def discount_percent(self) -> float:
        return self.__discount_percent

    @discount_percent.setter
    def discount_percent(self, new_percent: float) -> None:
        if not (0 <= new_percent <= 100):
            raise ValueError("Скидка должна быть от 0 до 100")
        self.__discount_percent = float(new_percent)

    @property
    def price(self) -> float:
        original_price = super().price
        discounted_price = original_price * (1 - self.discount_percent / 100)
        return max(0.0, discounted_price)

    def __str__(self) -> str:
        # return  f"Наименование: {self.__name}, Цена: {self.__price}, Количество: {self.__quantity}, ID: {self.product_id}"
        return f"{self.name} ({self.product_id}): {int(self.price)} руб. (скидка {self.discount_percent}%), в наличии: {self.quantity}"
