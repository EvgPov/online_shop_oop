from .customer import Customer

class Order:
    STATUSES = { "новый", "оплачен", "отправлен", "доставлен" }

    def __init__(self, order_id: str, customer: Customer, items: dict[str, int], total_price: float):
        self.order_id = order_id
        self.customer = customer
        self.items = items.copy()
        self.total_price = total_price
        self.status = "новый"

    # изменяет статус
    def update_status(self, new_status):
        if new_status not in self.STATUSES:
            raise ValueError("f Недопустимый статус: {new_status}")
        self.status = new_status

    # возвращает информацию о заказе
    def __str__(self) -> str:
        return (f"Заказ: {self.order_id}, Покупатель: {self.customer}, "
                f"Стоимость заказа: {self.total_price} руб., Статус: {self.status}")


