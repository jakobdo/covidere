import pytest
from tests import factories
from product.models import Product
from postcode.models import Postcode
from order.models import Order,OrderItem
from mixer.backend.django import mixer
from django.core.management import call_command

# Factory fixtures
@pytest.fixture
def user(db):
    return factories.UserFactory()

# Mixer fixtures
@pytest.fixture
def postcode(db):
    return mixer.blend(Postcode)


@pytest.fixture
def product(db):
    return mixer.blend(Product, image=None)


@pytest.fixture
def orderItem(db):
    return mixer.blend(OrderItem, Order = mixer.blend(Order), product = mixer.blend(Product, image=None))


@pytest.fixture
def order(db):
    return mixer.blend(Order)


@pytest.fixture(scope='session')
def django_db_setup_1(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'postcodes.json')
        call_command('loaddata', 'users.json')
        call_command('loaddata', 'shops.json')
        call_command('loaddata', 'active_products.json')
        call_command('loaddata', 'inactive_products.json')

