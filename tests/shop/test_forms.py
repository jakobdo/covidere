import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile

from shop.forms import ShopContactForm, ShopRegisterForm, ShopProductForm
from tests import factories


class TestShopContactForm:
    form = ShopContactForm

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
    def test_shop_contact_form(self, email, subject, message, validity):
        data = {
            'email': email,
            'subject': subject,
            'message': message
        }
        assert self.form(data=data).is_valid() == validity


class TestShopRegisterForm:
    form = ShopRegisterForm

    @pytest.mark.parametrize(
        'cvr_number, name, address, email, phone, postcode_special, city_special, validity',
        [
            (None,       'Name', 'Address 123', 'user1@email.tld', '43211234', '2000', 'City', False),
            ('12345678', None,   'Address 123', 'user2@email.tld', '43211234', '2000', 'City', False),
            ('12345678', 'Name', None,          'user3@email.tld', '43211234', '2000', 'City', False),
            ('12345678', 'Name', 'Address 123', 'user4@email.tld',  None,      '2000', 'City', False),
            ('12345678', 'Name', 'Address 123', 'user5@email.tld', '43211234', None,   'City', False),
            ('12345678', 'Name', 'Address 123', 'user6@email.tld', '43211234', '2000', None,   False),
            ('12345678', 'Name', 'Address 123', 'fake-email',      '43211234', '2000', 'City', False),
            ('12345678', 'Name', 'Address 123', 'user7@email.tld', '43211234', '2000', 'City', True),
        ]
    )
    def test_shop_register_form_validity(
        self,
        db,
        postcode,
        cvr_number,
        name,
        address,
        email,
        phone,
        postcode_special,
        city_special,
        validity
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
        form = self.form(data=data)
        assert form.is_valid() == validity


class TestShopProductForm:
    form = ShopProductForm

    @pytest.mark.parametrize(
        'name, description, price, offer_price, active, start_datetime, end_datetime, validity',
        [
            ('ProductName', 'Description', 100, 90, True, timezone.now() - timedelta(days=1), timezone.now() + timedelta(days=10), True),
            ('',            'Description', 100, 90, True, timezone.now() - timedelta(days=1), timezone.now() + timedelta(days=10), False),
            ('ProductName', '',            100, 90, True, timezone.now() - timedelta(days=1), timezone.now() + timedelta(days=10), False),
            ('ProductName', 'Description', -1,  90, True, timezone.now() - timedelta(days=1), timezone.now() + timedelta(days=10), False),
            ('ProductName', 'Description', 100, -1, True, timezone.now() - timedelta(days=1), timezone.now() + timedelta(days=10), False),
            ('ProductName', 'Description', 100, 90, True, timezone.now() + timedelta(days=5), timezone.now() + timedelta(days=1),  False),
        ]
    )
    def test_shop_product_form_validity(
        self,
        db,
        name,
        description,
        price,
        offer_price,
        active,
        start_datetime,
        end_datetime,
        validity
    ):
        testshop = factories.ShopFactory()
        data = {
            'name': name,
            'description': description,
            'price': price,
            'image' : SimpleUploadedFile(name='test_image.jpg', content=open('static/base/img/default_shop.jpg', 'rb').read(), content_type='image/jpeg'),
            'offer_price': offer_price,
            'active': active,
            'start_datetime': start_datetime,

            'end_datetime': end_datetime
        }
        form = self.form(data=data, user = testshop.user, files=data)
        result = form.is_valid()
        assert result == validity
