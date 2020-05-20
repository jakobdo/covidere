import pytest
from datetime import datetime
from mixer.backend.django import mixer
from django.core.exceptions import ValidationError
from tests.conftest import product

# Tests not yet implemented:
#   price=10, offer_price=9, updating price to 8 (test in shop:ShopProductUpdateView?)
#   inactive-manager & active-manager query returns correct counts

# Keep tests to form (non-functional) + model-class methods



def test_product_price(product):
    assert str(product) == product.name


@pytest.mark.parametrize(
    'price, offer_price, result',
    [
        (10, None, 10),
        (10, 999, 999), # Not much of an offer
        (10, 1, 1),
     ])
def test_product_get_price(product, price, offer_price, result):
    product.price = price
    product.offer_price = offer_price
    assert product.get_price() == result


#@pytest.mark.parametrize(
#    'start_datetime, end_datetime',
#    [
#        (datetime(2020,1,2), datetime(2020,1,1)),
#     ])
#def test_product_valid_datetimes(product, start_datetime, end_datetime):
#    product.start_datetime = start_datetime
#    product.end_datetime = end_datetime
#    with pytest.raises(ValidationError):
#        product.clean()
