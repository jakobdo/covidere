import pytest
from tests.conftest import product

from shop.forms import ShopContactForm, ShopRegisterForm, ShopProductForm


@pytest.mark.parametrize(
    'email, subject, message, validity',
    [
        (None, 'validSubject', 'validMessage', False),
        ('', 'validSubject', 'validMessage', False),
        ('example.com', 'validSubject', 'validMessage', False),

        ('valid@email.com', '', 'validMessage', False),
        ('valid@email.com', None, 'validMessage', False),
        ('valid@email.com', 'x' * 200, 'validMessage', False),

        ('valid@email.com', 'validMessage', '', False),
        ('valid@email.com', 'validMessage', None, False),
        ('valid@email.com', 'validMessage', 'x' * 10000, False),

        ('valid@email.com', 'validMessage', 'validMessage', True),
    ]
)
def test_contact_form_validity(email, subject, message, validity):
    form = ShopContactForm(data={
        'email': email,
        'subject': subject,
        'message': message
        })

    result = form.is_valid()
    assert result is validity



@pytest.mark.parametrize(
    'cvr_number, name, address, postcode_special, city_special, email, phone, validity',
    [
        ('43215678', 'validName', 'validAddress 1', '2000', 'Frederiksberg',  'valid@email.com', '43215678', True),
        ('4321567' , 'validName', 'validAddress 1', '2000', 'Frederiksberg',  'valid@email.com', '43215678', False),
        ('43215678', None       , 'validAddress 1', '2000', 'Frederiksberg',  'valid@email.com', '43215678', False),
        ('43215678', 'validName', None            , '2000', 'Frederiksberg',  'valid@email.com', '43215678', False),
        ('43215678', 'validName', 'validAddress 1', 'abcd', 'Frederiksberg',  'valid@email.com', '43215678', False),
        ('43215678', 'validName', 'validAddress 1', '2000', None           ,  'valid@email.com', '43215678', False),
        ('43215678', 'validName', 'validAddress 1', '2000', 'Frederiksberg',  'invalid.com'    , '43215678', False),
        ('43215678', 'validName', 'validAddress 1', '2000', 'Frederiksberg',  'valid@email.com', 'x'*99    , False),
    ]
)
def test_shop_register_form_validity(cvr_number, name, address, postcode_special, city_special, email, phone, validity, db):
    form = ShopRegisterForm(data={
        'cvr_number': cvr_number,
        'name': name,
        'address': address,
        'postcode_special': postcode_special,
        'city_special': city_special,
        'email': email,
        'phone': phone,
        })

    result = form.is_valid()
    assert result is validity


## Test "offer_price !> price" & "end_datetime !< start_datetime"
## Not implemented yet due to complexity of task
#@pytest.mark.parametrize( 
#    'price, offer_price, start_datetime, end_datetime, validity',
#    [
#        (10, 11, None, None, False),
#        (None, None, None, None, False),
#        (10, -11, None, None, False),
#        (-1, None, None, None, False),
#        (1, -1, None, None, False),
#        (10, None, Datetime(2020,1,2), datetime(2020,1,1), False),
#    ]
#)
#def test_shop_product_form_validity(product, price, offer_price, start_datetime, end_datetime, validity, db):
#    form = ShopProductForm()
#    result = form.is_valid()
#    assert result is validity