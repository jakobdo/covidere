import pytest
from tests import factories

@pytest.fixture
def user(db):
    return factories.UserFactory()
