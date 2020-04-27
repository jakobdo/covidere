from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy


class User(AbstractUser):
    email = models.EmailField(gettext_lazy('email address'), unique=True)

    class Meta:
        permissions = (
            ("alten_admin", "Can administrate shops in Alten Admin"),
        )
