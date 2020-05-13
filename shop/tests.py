from django.test import TestCase
from django.urls import reverse, resolve

class TestUrls:

    def test_shops_url_resolves(self):
        path = reverse('shops')

        assert resolve(path).view_name == 'shop'