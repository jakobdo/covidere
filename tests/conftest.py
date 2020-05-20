import pytest
from tests import factories
from product.models import Product
from mixer.backend.django import mixer


@pytest.fixture
def user(db):
    return factories.UserFactory()


@pytest.fixture
def product(db):
    return mixer.blend(Product, image=None)
