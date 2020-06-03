import pytest

from product.models import Product

from tests import factories


def test_product_str_repr(product):
    assert str(product) == product.name


@pytest.mark.parametrize(
    'price, offer_price, result',
    [
        (10, None, 10),
        (10, 999, 999),
        (10, 1, 1),
    ])
def test_product_get_price(product, price, offer_price, result):
    product.price = price
    product.offer_price = offer_price
    assert product.get_price() == result

def test_product_custom_managers(db):
    inactive_products = factories.ProductFactory.create_batch(2, active=False)
    active_products = factories.ProductFactory.create_batch(2, active=True)
    assert Product.actives.count() == 2
    assert Product.inactives.count() == 2
    assert Product.objects.count() == 4
