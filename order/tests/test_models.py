import pytest
from tests.conftest import orderItem


@pytest.mark.parametrize(
    'price, count, result',
    [
        (10, 1, 10),
        (10, 100, 1000),
     ])
def test_orderItem_subtotal(orderItem, price, count, result):
    orderItem.count = count
    orderItem.price = price
    assert orderItem.subtotal() == result





