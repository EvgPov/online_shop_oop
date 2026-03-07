from .order import Order

class PaymentProcessor:
    def process_payment (self, order: Order, amount:float) -> bool:
        raise NotImplementedError

# CreditCardProcessor
class CreditCardProcessor(PaymentProcessor):
    def process_payment (self, order: Order, amount: float) -> str:
        message = f"Оплата заказа {order.order_id} на сумму {int(amount)} прошла по кредитной карте."
        print(message)
        return message

# PayPalProcessor
class PayPalProcessor(PaymentProcessor):
    def process_payment (self, order: Order, amount: float) -> str:
        message = f"Оплата заказа {order.order_id} на сумму {int(amount)} прошла по PayPal."
        print(message)
        return message