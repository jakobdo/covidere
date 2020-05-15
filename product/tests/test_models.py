import pytest
from datetime import datetime
from mixer.backend.django import mixer

from product.models import Product


@pytest.fixture
def offer_product(request, db):
    return mixer.blend(Product, image=None, price=10, offer_price=request.param)

@pytest.fixture
def product(request, db):
    return mixer.blend(Product, image=None)


@pytest.mark.parametrize('offer_product', [9.99,-10], indirect=True)
def test_product_price_is_gt_offer_price(offer_product):
    assert offer_product.price > offer_product.offer_price

@pytest.mark.parametrize('offer_product', [10], indirect=True)
def test_product_price_not_gt_offer_price(offer_product):
    assert not offer_product.price > offer_product.offer_price

@pytest.mark.parametrize(
    'start_datetime, end_datetime, validity',
    [
        (datetime(2020,1,1), datetime(2020,1,1), False),
        (datetime(2020,1,1), datetime(2019,12,31), False),

    ])
def test_product_valid_datetimes(product, start_datetime, end_datetime, validity):
    product.start_datetime = start_datetime
    product.end_datetime = end_datetime
    assert (product.start_datetime < product.end_datetime) is validity
