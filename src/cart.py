from .customer import Customer
from .product import Product

class Cart:
    def __init__(self, customer: Customer):
        self.customer = customer
        self.items: dict[Product, int] = {}
    # добавление товара в корзину
    def add_item(self, product: Product, quantity: int = 1):
        if quantity <= 0:
            return
        if not product.is_available(quantity):
            raise ValueError(
                f"Недостаточно '{product.name} на складе' (в наличии {product.quantity})"
            )
        if product in self.items:
            self.items[product] += quantity
        else:
            self.items[product] = quantity
    # удаление товара из корзины
    def remove_item(self, product_id: str):
        for product in list(self.items.keys()):
            if product.product_id == product_id:
                self.items.pop(product)
                return

    # изменение количество товара в корзине
    def update_quantity(self, product_id: str, new_quantity: int)-> int:
        if new_quantity <= 0:
            self.remove_item(product_id)
            return
        for product in self.items:
            if product.product_id == product_id:
                if not product.is_available(new_quantity):
                    raise ValueError(
                        f"Недостаточно товара '{product.name}' нам складе"
                        f"в наличии {product.quantity}"
                    )
                self.items[product] = new_quantity
                return

    # вычисление общей стоимости товаров в корзине
    def get_total_price(self, product_catalog: dict[str, Product]) -> float:
        total_price = 0.0
        for product, quantity in self.items.items():
            current_product = product_catalog.get(product.product_id)
            if current_product:
                total_price += current_product.price * quantity
            else:
                total_price += product.price * quantity
        return total_price

    # очищение корзины
    def clear_cart(self):
        self.items.clear()

    # содержимое корзины
    def __str__(self):
        if not self.items:
            return f"Корзина {self.customer.name} пуста"

        lines = [f"Корзина {self.customer.name}:", ""]
        total_quantity = sum(self.items.values())

        for product, quantity in sorted(self.items.items(), key=lambda item: item[0].name):
            lines.append(f"  {product.product_id} × {quantity} шт. ({product.name})")
        lines.append("")
        lines.append(f"Всего позиций: {len(self.items)}  Всего товаров: {total_quantity:>4}")
        return "\n".join(lines)

