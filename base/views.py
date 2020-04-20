from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import Http404, redirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext
from django.views.generic import FormView

from base.forms import SetPasswordForm
from base.models import User
from shop.forms import PostCodeForm
from shop.models import Postcode
from shop.tokens import account_activation_token


class ActivateUserView(FormView):
    template_name = 'base/set_password.html'
    form_class = SetPasswordForm

    def validate_user(self):
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs.get('uidb64')))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.user = None
    
    def validate_token(self):
        return self.user is not None and self.user.is_active is False and account_activation_token.check_token(self.user, self.kwargs.get('token'))

    def form_valid(self, form):
        self.validate_user()

        if self.validate_token():
            user = self.user
            user.is_active = True
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(self.request, user)
        else:
            raise Http404(gettext("Invalid token"))
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.validate_user()
        if not self.validate_token():
            raise Http404(gettext("Invalid token"))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('shop_overview')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        #user.is_active = True
        #user.save()
        login(request, user)
        return HttpResponse(f"<html><head><title>Test</title></head><body>{token}</body></html>")
        #return redirect('set_password')
        #return redirect('shop_overview')
    else:
        raise Http404(gettext("Invalid token"))


class PostCodeView(FormView):
    template_name = 'base/postcode.html'
    form_class = PostCodeForm

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        url = f"{settings.PROTOCOL}://{self.form.cleaned_data.get('postcode').postcode}.{settings.DOMAIN_NAME}{reverse('index')}"
        return url


def postcodes(request):
    q = request.GET.get('q')
    try:
        code = Postcode.objects.get(postcode=q, active=True)
    except (Postcode.DoesNotExist, ValueError):
        return JsonResponse({'error': gettext("Postcode not found")}, status=400)
    return JsonResponse(
        dict(
            city=code.city,
            id=code.pk
        )
    )
