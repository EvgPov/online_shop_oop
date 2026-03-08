from src.customer import Customer
from src.shop import Shop
from src.payment_processor import CreditCardProcessor
from src.payment_processor import PayPalProcessor
from src.product import Product
from src.product import DigitalProduct
from src.product import DiscountedProduct

from datetime import date

if __name__ == '__main__':
    shop = Shop()

    # добавление товаров
    shop.add_product(Product("Джинсы мужские", 15000.00, 10, "T001" ))
    shop.add_product(Product("Кроссовки", 24000.00, 15, "T002"))
    shop.add_product(Product("Куртка", 35000.00, 12, "T003"))

    shop.add_product(DigitalProduct("Курс Python", 4900.00, 1000, "DIG001", 2.5, "http://..."))
    shop.add_product(DigitalProduct("Курс JavaScript", 6900.00, 1000, "DIG002", 5.7, "http://..."))
    shop.add_product(DigitalProduct("Курс React", 9900.00, 1000, "DIG003", 15.8, "http://..."))

    shop.add_product(DiscountedProduct("Пуховик", 49000.00, 5, "S001", 30))
    shop.add_product(DiscountedProduct("Сапоги", 7900.00, 3, "S002", 50))
    shop.add_product(DiscountedProduct("Шапка", 8900.00, 1, "S003", 20))
    shop.add_product(DiscountedProduct("Джинсы женские", 10900.00, 10, "S004", 35))

    shop.display_products()

    # регистрация клиента
    client1_thomas = Customer("Thomas Edison", "C001", 'customer@example.ru')
    client2_john = Customer("John Lennon", "C002", 'john@example.ru')
    client3_robert = Customer("Robert De Niro", "C003", 'robert@example.ru')
    client4_morgan = Customer("Morgan Freeman", "C004", 'morgant@example.ru')

    shop.register_customer(client1_thomas)
    shop.register_customer(client2_john)
    shop.register_customer(client3_robert)
    shop.register_customer(client4_morgan)

    # создаем корзину
    cart_thomas = shop.get_cart(client1_thomas)
    cart_john = shop.get_cart(client2_john)
    cart_robert = shop.get_cart(client3_robert)
    cart_morgan = shop.get_cart(client4_morgan)

    # добавление товаров в корзины
    cart_thomas.add_item(shop["T001"])
    cart_thomas.add_item(shop["T002"])
    cart_thomas.add_item(shop["DIG001"])
    cart_thomas.add_item(shop["S001"])

    cart_john.add_item(shop["T003"])
    cart_john.add_item(shop["DIG002"])
    cart_john.add_item(shop["DIG003"])
    cart_john.add_item(shop["S002"])
    cart_john.add_item(shop["S002"])

    cart_robert.add_item(shop["T001"], 2)
    cart_robert.add_item(shop["T002"], 3)
    cart_robert.add_item(shop["T003"])
    cart_robert.add_item(shop["DIG003"])
    cart_robert.add_item(shop["S001"])
    cart_robert.add_item(shop["S003"])

    cart_morgan.add_item(shop["T003"], 2)
    cart_morgan.add_item(shop["T001"], 2)
    cart_morgan.add_item(shop["DIG001"])
    cart_morgan.add_item(shop["S001"], 1)

    # вывод содержимого корзин
    print()
    print(cart_thomas)
    print()
    print(cart_john)
    print()
    print(cart_robert)
    print()
    print(cart_morgan)

    # оформление заказов
    print()
    order_thomas = shop.create_order(client1_thomas,  CreditCardProcessor())
    order_john = shop.create_order(client2_john, PayPalProcessor())
    order_robert = shop.create_order(client3_robert, PayPalProcessor())
    # вывод состава заказа
    print()
    print(order_thomas)
    print(order_john)
    print(order_robert)

    # проверка остатков после заказа
    print()
    print("Остатки после заказаов:")
    shop.display_products()

    # Поиск товаров
    print()
    print("Поиск по слову 'джинсы':")
    for product in shop.find_products_by_name('джинсы'):
        print(product)
    # сохранение в файл
    today_str = date.today().isoformat()
    filename = f"backup_{today_str}.json"

    print()
    shop.save_to_json(filename)

    shop2 = Shop()
    #загрузка из файла
    shop2.load_from_json(filename)

    print("После загрузки:")
    print(f"Товаров: {len(shop2.products)}")
    print(f"Клиентов: {len(shop2.customers)}")
    print(f"Заказов: {len(shop2.orders)}")
    print(f"Корзин: {len(shop2.carts)}")
















