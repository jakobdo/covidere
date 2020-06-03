import factory
from datetime import timedelta
from tests import factoryutils
from django.contrib.gis.geos import Point
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.User'

    username = factory.Sequence(lambda number: f"user{number}")
    email = factory.Sequence(lambda number: f"user{number}@domain.tld")


class PostcodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'postcode.Postcode'
        django_get_or_create = ('postcode',)
    
    postcode = 2000
    city = 'Frederiksberg'
    location = Point(12, 34)
    active = True


class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'shop.Shop'

    name = factory.Sequence(lambda n: 'Shop name {0}'.format(n))
    address = factory.Sequence(lambda n: 'Address {0}'.format(n))
    postcode = factory.SubFactory(PostcodeFactory)
    homepage = factory.Sequence(lambda n: 'www.homepage_{0}.com'.format(n))
    email = factory.Sequence(lambda n: 'addres_{0}@example.com'.format(n))
    phone = factory.Sequence(lambda n: "1{:07d}".format(n)) 
    user = factory.SubFactory(UserFactory, username = factory.Sequence(lambda n: "Agent %03d" % n))
    cvr_number = factory.Sequence(lambda n: "1{:07d}".format(n))  
    active = True
    order_pickup = True
    delivery_range = -1
    shop_image = None
    location = factoryutils.FuzzyPoint()


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'product.Product'

    shop = factory.SubFactory(ShopFactory)
    name = factory.Sequence(lambda n: 'Product Name {0}'.format(n))
    description = factory.Sequence(lambda n: 'Product Description {0}'.format(n))
    price = factory.Sequence(lambda n: 99.95 + 10*n)
    offer_price = None
    image = None
    active = True
    start_datetime = timezone.now() - timedelta(days=1)
    end_datetime = start_datetime + timedelta(days=10)


class InactiveProduct(ProductFactory):
    active = False


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'order.Order'

    name = factory.Sequence(lambda n: 'Order no. {0}'.format(n))
    postcode = factory.SubFactory(PostcodeFactory)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'order.OrderItem'

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    count = factory.Sequence(lambda n: n)
    price = factory.Sequence(lambda n: 99.95 + 10*n)

