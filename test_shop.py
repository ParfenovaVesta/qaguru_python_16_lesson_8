"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_new():
    return Product("dress", 200, "This is a dress", 5)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):  # Проверяем количество товара
        assert product.check_quantity(500) == True
        assert product.check_quantity(2000) == False

    def test_product_buy(self, product):  # Покупаем товар
        count = product.quantity - 10
        product.buy(count)
        assert product.quantity == 10

    def test_product_buy_more_than_available(self, product):  # Покупаем товара больше, чем есть в наличии
        with pytest.raises(ValueError, match='Недостаточно товара'):
            product.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):  # Добавляем товар в корзину
        cart.add_product(product)
        assert cart.products[product] == 1

        cart.add_product(product, buy_count=3)
        assert cart.products[product] == 4

    def test_remove_product(self, cart, product):  # Удаляем товар из корзины
        cart.add_product(product)
        cart.remove_product(product)
        assert product not in cart.products

    def test_cart_remove_one_product(self, cart, product):  # Убираем часть товара из корзины

        cart.add_product(product, buy_count=2)
        cart.remove_product(product, remove_count=1)
        assert cart.products[product] == 1

    def test_clear(self, cart, product, product_new):  # Очищаем корзину полностью
        cart.add_product(product)
        cart.add_product(product_new)
        cart.clear()
        assert product not in cart.products
        assert product_new not in cart.products

    def test_get_total_price(self, cart, product, product_new):  # Проверяем итоговую стоимость
        cart.add_product(product)
        cart.add_product(product_new, buy_count=2)
        assert cart.get_total_price() == 500

    def test_buy_ok(self, cart, product_new):
        cart.add_product(product_new)
        cart.buy()

    def test_buy_nok(self, cart, product_new):
        cart.add_product(product_new, buy_count=6)
        with pytest.raises(ValueError, match='Недостаточно товара'):
            cart.buy()
