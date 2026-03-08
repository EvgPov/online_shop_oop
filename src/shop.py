from .product import Product
from .product import DigitalProduct
from .product import DiscountedProduct
from .cart import Cart
from .customer import Customer
from .order import Order
from .payment_processor import PaymentProcessor

import json
from pathlib import Path

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
        order = Order(order_id, customer, items_for_order, total)
        # order_items = items_for_order
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
            print(f"{product.product_id}: {product.name}, Цена: {product.price}, Количество: {product.quantity}")

    def __len__(self):
        return len(self.products)

    def __getitem__(self, key: str | int) -> Product:
        if isinstance(key, str):
            return self.products.get(key)
        if isinstance(key, int):
            return list(self.products.values())[key]
        raise TypeError("Ожидается str (id) или int (индекс)")

    # сохранение состояния магазина в json
    def save_to_json(self, filename: str = "shop_data.json"):
        data = {
            "products": {},
            "customers": {},
            "orders": [],
            "carts": {}
        }
        # сохранение товаров
        for product_id, product in self.products.items():
            product_data = {
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "product_id": product.product_id,
            }
            if isinstance(product, DigitalProduct):
                product_data["type"] = "digital"
                product_data["file_size"] = product.file_size
                product_data["download_link"] = product.download_link
            elif isinstance(product, DigitalProduct):
                product_data["type"] = "discounted"
                product_data["discount_percent"] = product.discount_percent
            else:
                product_data["type"] = "regular"

            data["products"][product_id] = product_data

        # сохранение покупателей
        for customer_id, customer in self.customers.items():
            data["customers"][customer_id] = {
                "name": customer.name,
                "customer_id": customer.customer_id,
                "email": customer.email,
            }
        # сохранение заказов
        for order in self.orders:
            data["orders"].append({
                "order_id": order.order_id,
                "customer_id": order.customer.customer_id,
                "items": order.items.copy(),
                "total_price": order.total_price,
                "status": order.status,
            })
        # сохранение корзин
        for customer_id, cart in self.carts.items():
            data["carts"][customer_id] = {
                "customer_id": customer_id,
                "items": {p.product_id: q for p, q in cart.items.items()},
            }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Данные сохранены в {filename}")

    #загрузка состояния магазина из json
    def load_from_json(self, filename: str = "shop_data.json"):
        if not Path(filename).exists():
            print("Файл не найден")
            return

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # очищаем текущее состояние
        self.products.clear()
        self.customers.clear()
        self.orders.clear()
        self.carts.clear()

        # загружаем товары
        for product_id, product_data in data.get("products", {}).items():
            if product_data.get("type") == "digital":
                product = DigitalProduct(
                    name=product_data.get("name"),
                    price=product_data.get("price"),
                    quantity=product_data.get("quantity"),
                    product_id=product_id,
                    file_size=product_data.get("file_size"),
                    download_link=product_data.get("download_link"),
                )
            elif product_data.get("type") == "discounted":
                product = DiscountedProduct(
                    name=product_data.get("name"),
                    price=product_data.get("price"),
                    quantity=product_data.get("quantity"),
                    product_id=product_id,
                    discount_percent=product_data.get("discount_percent"),
                )
            else:
                product = Product(
                    name=product_data.get("name"),
                    price=product_data.get("price"),
                    quantity=product_data.get("quantity"),
                    product_id=product_id,
                )
            self.products[product_id] = product

        # загружаем покупателей
        for customer_id, customer_data in data.get("customers", {}).items():
            customer = Customer(
                name=customer_data.get("name"),
                customer_id=customer_id,
                email=customer_data.get("email"),
            )
            self.customers[customer_id] = customer

        # загрузка корзин
        for customer_id, cart_data in data.get("carts", {}).items():
            if customer_id not in self.customers:
                print(f"Покупатель {customer_id} не найден для корзины")
                continue
            customer = self.customers[customer_id]
            cart = Cart(customer)

            for product_id, quantity in cart_data.get("items", {}).items():
                product = self.products.get(product_id)
                if product:
                    current_quantity = cart.items.get(product, 0)
                    cart.items[product] = current_quantity + quantity
                else:
                    print(f"Товар {product_id} не найден при восстановлении корзины {customer_id}")
            self.carts[customer_id] = cart

        # загрузка заказов
        for order_data in data.get("orders", []):
            customer_id = order_data.get("customer_id")
            if customer_id not in self.customers:
                print(f"Покупатель {customer_id} не найден для заказа {order_data['order_id']}")
            customer = self.customers[customer_id]

            # загружаем items как {Product: quantity}
            restorted_items = {}
            for product_id, quantity in order_data.get("items", {}).items():
                product = self.products.get(product_id)
                if product:
                    restorted_items[product] = quantity
                else:
                    print(f"Товар {product_id} не найден в заказе {order_data['order_id']}")

            order = Order(
                order_id=order_data.get("order_id"),
                customer=customer,
                items=restorted_items,
                total_price=order_data.get("total_price"),
            )
            order.status = order_data.get("status", "новый")
            self.orders.append(order)

            # обновляем счетчик заказо, если нужно
            try:
                num = int(order_data["order_id"].split("-")[-1])
                self._next_order_id = max(self._next_order_id, num + 1)
            except:
                pass
        print(f"Данные успешно загружены из {filename}")
        print()
        print(f"Товаров: {len(self.products)}")
        for product in self.products.values():
            print(product)
        print()
        print(f"Клиентов: {len(self.customers)}")
        for customer in self.customers.values():
            print(customer)
        print()
        print(f"Заказов: {len(self.orders)}")
        for order in self.orders:
            print(order)
        print()
        print(f"Корзин: {len(self.carts)}")
        for cart in self.carts.values():
            print(cart)