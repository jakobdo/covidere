from django.contrib.auth import login
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import Http404
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext
from django.views.generic import FormView

from base.forms import SetUsernameAndPasswordForm
from base.models import User
from shop.tokens import account_activation_token


class ActivateUserView(FormView):
    template_name = 'base/set_password.html'
    form_class = SetUsernameAndPasswordForm

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
            user.username = form.cleaned_data["username"]
            user.set_password(form.cleaned_data["password1"])
            try:
                user.save()
            except IntegrityError:
                form.add_error('username', gettext('Shop with this username already exists.'))
                return super(ActivateUserView, self).form_invalid(form)

            login(self.request, user, backend='axes.backends.AxesBackend')
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
