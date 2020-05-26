import pytest
from tests import factories
from django.core.management import call_command


@pytest.fixture
def user(db):
    return factories.UserFactory()


@pytest.fixture
def postcode(db):
    return factories.PostcodeFactory()


@pytest.fixture
def product(db):
    return factories.ProductFactory()


@pytest.fixture
def orderItem(db):
    return factories.OrderItemFactory()


@pytest.fixture
def order(db):
    return factories.OrderFactory()


# Populate test db with existing fixture .json files
@pytest.fixture(scope='session')
def django_db_setup_1(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'postcodes.json')
        call_command('loaddata', 'users.json')
        call_command('loaddata', 'shops.json')
        call_command('loaddata', 'active_products.json')
        call_command('loaddata', 'inactive_products.json')

