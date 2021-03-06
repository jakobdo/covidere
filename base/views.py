from django.contrib.auth import login
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import Http404
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext, ugettext
from django.views import View
from django.views.generic import FormView, TemplateView

from base.forms import SetUsernameAndPasswordForm
from base.models import User
from shop.tokens import account_activation_token


class AboutPageView(TemplateView):
    template_name = 'about.html'


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': ugettext('Health-check: OK')})


class ActivateUserView(FormView):
    template_name = 'base/set_password.html'
    form_class = SetUsernameAndPasswordForm

    def validate_token(self):
        return (
            self.user.is_active is False and
            account_activation_token.check_token(
                self.user,
                self.kwargs.get('token')
            )
        )

    def get_form_kwargs(self):
        kwargs = super(ActivateUserView, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = self.user
        user.is_active = True
        user.username = form.cleaned_data["username"]
        user.set_password(form.cleaned_data["password1"])
        try:
            user.save()
        except IntegrityError:
            form.add_error(
                'username',
                gettext('Shop with this username already exists.')
            )
            return super(ActivateUserView, self).form_invalid(form)

        login(self.request, user, backend='axes.backends.AxesBackend')
        return super().form_valid(form)

    def setup(self, request, *args, **kwargs):
        super(ActivateUserView, self).setup(request, *args, **kwargs)
        try:
            uid = force_text(urlsafe_base64_decode(kwargs.get('uidb64')))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise Http404(gettext("Invalid token"))
        if not self.validate_token():
            raise Http404(gettext("Invalid token"))

    def get_success_url(self):
        return reverse('shop_overview')
