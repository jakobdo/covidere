import pytest

from shop.forms import ShopContactForm, ShopRegisterForm


class TestShopContactForm:
    form = ShopContactForm

    @pytest.mark.parametrize(
        'email, subject, message, result',
        [
            (None, 'Subject', 'Message', False),
            ('fake-email', 'Subject', 'Message', False),
            ('user@email.tld', None, 'Message', False),
            ('user@email.tld', 'Subject', None, False),
            ('user@email.tld', 'Subject', 'Message', True),
        ]
    )
    def test_shop_contact_form(self, email, subject, message, result):
        data = {
            'email': email,
            'subject': subject,
            'message': message
        }
        assert self.form(data=data).is_valid() == result


class TestShopRegisterForm:
    form = ShopRegisterForm

    @pytest.mark.parametrize(
        'cvr_number, name, address, email, phone, postcode_special, city_special, result',
        [
            (None, 'Name', 'Address 123', 'user@email.tld', '43211234', '1234', 'City', False),
            ('12345678', None, 'Address 123', 'user@email.tld', '43211234', '1234', 'City', False),
            ('12345678', 'Name', None, 'user@email.tld', '43211234', '1234', 'City', False),
            ('12345678', 'Name', 'Address 123', 'user@email.tld',  None, '1234', 'City', False),
            ('12345678', 'Name', 'Address 123', 'user@email.tld', '43211234', None, 'City', False),
            ('12345678', 'Name', 'Address 123', 'user@email.tld', '43211234', '1234', None, False),
            ('12345678', 'Name', 'Address 123', 'fake-email', '43211234', '1234', 'City', False),
            ('12345678', 'Name', 'Address 123', 'user@email.tld', '43211234', '1234', 'City', True),
        ]
    )
    def test_shop_register__form(
        self,
        cvr_number,
        name,
        address,
        email,
        phone,
        postcode_special,
        city_special,
        result
    ):
        data = {
            'cvr_number': cvr_number,
            'name': name,
            'address': address,
            'email': email,
            'phone': phone,
            'postcode_special': postcode_special,
            'city_special': city_special
        }
        assert self.form(data=data).is_valid() == result
