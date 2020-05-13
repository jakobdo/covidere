import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.User'
        django_get_or_create = ('username',)

    username = 'john'
