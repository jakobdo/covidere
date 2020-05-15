import pytest
from datetime import datetime
from mixer.backend.django import mixer
from django.core.exceptions import ValidationError

from product.models import Product


@pytest.fixture
def product(db):
    return mixer.blend(Product, image=None)

@pytest.mark.parametrize(
    'price, offer_price',
    [
        (10, 10),
        #(None, None), # Does a price have to be defined?
        (10, 999),
        (-1, None),
        (1, -1),
     ])
def test_product_price_and_offer_price(product, price, offer_price):
    product.price = price
    product.offer_price = offer_price
    with pytest.raises(ValidationError):
        product.full_clean() 

@pytest.mark.parametrize(
    'start_datetime, end_datetime',
    [
        (datetime(2020,1,2), datetime(2020,1,1)),
     ])
def test_product_valid_datetimes(product, start_datetime, end_datetime):
    product.start_datetime = start_datetime
    product.end_datetime = end_datetime
    with pytest.raises(ValidationError):
        product.clean()
