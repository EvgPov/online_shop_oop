from .product import Product
from .product import DigitalProduct
from .cart import Cart
from .customer import Customer
from .order import Order
from .payment_processor import PaymentProcessor

class Shop:
    def __init__(self):
        self.products: dict[str, Product] = {}
        self.customers: dict[str, Customer] = {}
        self.orders: list[Order] = []
        self.carts: dict[str, Cart] = {}
        self._next_order_id = 10001

    # добавление товара в ассортимент
    def add_product(self, product: Product):
        if product.product_id in self.products:
            raise ValueError(f"ID {product.product_id} уже есть в каталоге товаров")
        self.products[product.product_id] = product

    # регистрация покупателя
    def register_customer(self, customer: Customer ):
        if customer.customer_id in self.customers:
            raise ValueError(f"Клиент с ID  { customer.customer_id } уже зарегистрирован")
        self.customers[customer.customer_id] = customer

    # корзина покупателя
    def get_cart(self, customer: Customer):
        if customer.customer_id not in self.carts:
            self.carts[customer.customer_id] = Cart(customer)
        return self.carts[customer.customer_id]

    # создание заказа из корзины покупателя
    # уменьшение количества товаров на складе
    #  очищение корзины
    # добавление заказа в список
    def create_order(self, customer: Customer, payment_processor: PaymentProcessor | None = None) -> Order:
        cart = self.get_cart(customer)
        if not cart.items:
            raise ValueError('Корзина пуста')

        total = cart.get_total_price(self.products)
        # Проверка наличия товаров
        items_for_order = {}
        for product, quantity in cart.items.items():
            items_for_order[product.product_id] = quantity
            if not isinstance(product, DigitalProduct):
                if product.quantity < quantity:
                    raise ValueError(
                         f"Недостаточно товара '{product.name}' на складе "
                        f"(в наличии {product.quantity}, запрошено {quantity})"
                    )
                product.quantity -= quantity

        order_id = f"ORDER-{ self._next_order_id }"
        self._next_order_id += 1

        # создание заказа из корзины покупателя
        order = Order(order_id, customer,items_for_order, total)
        # добавление заказа в список
        self.orders.append(order)

        if payment_processor:
            if payment_processor.process_payment(order, total):
                order.update_status("оплачен")

        # очищение корзины
        cart.clear_cart()
        return order

    # поиск товаров по части названия
    def find_products_by_name(self, name: str) -> list[Product]:
        low_name = name.lower()
        return [product for product in self.products.values() if low_name in product.name.lower()]

    # выводит список всех товаров с ценами и остатками.
    def display_products(self):
        if not self.products:
            print('Магазин пуст')
            return
        print('Ассортимент магазина')
        for product in sorted(self.products.values(), key=lambda x: x.name):
            print(f"{product.product_id}: {product.name}")

    def __len__(self):
        return len(self.products)

    def __getitem__(self, key: str | int) -> Product:
        if isinstance(key, str):
            return self.products.get(key)
        if isinstance(key, int):
            return list(self.products.values())[key]
        raise TypeError("Ожидается str (id) или int (индекс)")