import factory

from django.contrib.gis.geos import Point


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.User'
        django_get_or_create = ('username',)

    username = 'john'


class PostcodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'postcode.Postcode'

    postcode = 1234
    city = "City"
    location = Point(12, 34)
    active = True
