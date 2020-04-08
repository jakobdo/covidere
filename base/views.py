from django.contrib.auth import login
from django.shortcuts import Http404, redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext

from base.models import User
from shop.tokens import account_activation_token


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('shop_overview')
    else:
        raise Http404(gettext("Invalid token"))
