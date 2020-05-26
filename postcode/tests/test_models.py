import pytest
from tests.conftest import postcode


@pytest.mark.parametrize(
    'postcode_nmbr, city, result',
    [
        (1, "TownsVille", "1 - TownsVille"),
        (2000, "", "2000 - "),
     ])
def test_postcode_str(postcode, postcode_nmbr, city, result):
    postcode.postcode = postcode_nmbr
    postcode.city = city
    assert str(postcode) == result







