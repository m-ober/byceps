"""
:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from decimal import Decimal

from byceps.services.shop.cart.models import Cart
from byceps.services.shop.order import service as order_service
from byceps.services.shop.order.transfer.models import PaymentMethod

from testfixtures.shop_order import create_orderer

from tests.helpers import create_email_config, create_user_with_detail
from tests.services.shop.base import ShopTestBase


class OrderTotalAmountTest(ShopTestBase):

    def setUp(self):
        super().setUp()

        user = create_user_with_detail()
        self.orderer = create_orderer(user)

        create_email_config()

        self.shop = self.create_shop()
        self.create_order_number_sequence(self.shop.id, 'LF-01-B')

        self.article1 = self.create_article(1, Decimal('49.95'))
        self.article2 = self.create_article(2, Decimal( '6.20'))
        self.article3 = self.create_article(3, Decimal('12.53'))

    def test_without_any_items(self):
        order = self.place_order([])

        assert_decimal_equal(order.total_amount, Decimal('0.00'))

    def test_with_single_item(self):
        order = self.place_order([
            (self.article1, 1),
        ])

        assert_decimal_equal(order.total_amount, Decimal('49.95'))

    def test_with_multiple_items(self):
        order = self.place_order([
            (self.article1, 3),
            (self.article2, 1),
            (self.article3, 4),
        ])

        assert_decimal_equal(order.total_amount, Decimal('206.17'))

    # helpers

    def create_article(self, number, price):
        item_number = f'LF-01-A{number:05d}'
        description = f'Artikel #{number:d}'

        return super().create_article(
            self.shop.id,
            item_number=item_number,
            description=description,
            price=price,
            quantity=50,
        )

    def place_order(self, articles):
        payment_method = PaymentMethod.bank_transfer

        cart = Cart()
        for article, quantity in articles:
            cart.add_item(article, quantity)

        order, _ = order_service.place_order(
            self.shop.id, self.orderer, payment_method, cart
        )

        return order


def assert_decimal_equal(actual, expected):
    assert isinstance(actual, Decimal)
    assert actual == expected
