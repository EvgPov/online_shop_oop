from order import Order

class PaymentProcessor:
    def process_payment(self, order: Order, amount:float) -> bool:
        raise NotImplementedError

# CreditCardProcessor
class  CreditCardProcessor(PaymentProcessor):
    def process(self, order: Order, amount: float) -> bool:
        print(f"  → [Карта] Успешно оплачено {amount:} руб. (заказ {order.order_id})")
        return True

# PayPalProcessor
class PayPalProcessor(PaymentProcessor):
    def process(self, order: Order, amount: float) -> bool:
        print(f"  → [[PayPal] Успешно оплачено {amount:} руб. (заказ {order.order_id})")
        return True