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
    'name, email, phone, cvr_number, validity',
    [
        (None, 'valid@email.com', '43215678', '43215678', False),
        ('', 'valid@email.com', '43215678', '43215678', False),
        ('x' * 101, 'valid@email.com', '43215678', '43215678', False),

        ('validName', None, '43215678', '43215678', False),
        ('validName', '', '43215678', '43215678', False),

        ('validName', 'valid@email.com', 'a3215678', '43215678', False),
        ('validName', 'valid@email.com', '', '43215678', False),
        ('validName', 'valid@email.com', None, '43215678', False),

        ('validName', 'valid@email.com', '43215678', '3215678', False),
        ('validName', 'valid@email.com', '43215678', '432156789', False),

        ('validName', 'valid@email.com', '43215678', '43215678', True),
    ]
)
def test_shop_register_form_validity(name, email, phone, cvr_number, validity, db):
    form = ShopRegisterForm(data={
        'name': name,
        'email': email,
        'phone': phone,
        'cvr_number': cvr_number,
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