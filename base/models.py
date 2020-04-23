from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        permissions = (
            ("alten_admin", "Can administrate shops in Alten Admin"),
        )
