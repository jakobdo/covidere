from urllib.parse import unquote

from django.conf import settings
from django.contrib.auth import login
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import Http404
from django.urls import reverse, translate_url
from django.utils.encoding import force_text
from django.utils.http import (url_has_allowed_host_and_scheme,
                               urlsafe_base64_decode)
from django.utils.translation import (LANGUAGE_SESSION_KEY, check_for_language,
                                      gettext)
from django.views.generic import FormView, TemplateView

from base.forms import SetUsernameAndPasswordForm
from base.models import User
from shop.tokens import account_activation_token


class AboutPageView(TemplateView):
    template_name = 'about.html'


class ActivateUserView(FormView):
    template_name = 'base/set_password.html'
    form_class = SetUsernameAndPasswordForm

    def validate_token(self):
        return self.user.is_active is False and account_activation_token.check_token(self.user, self.kwargs.get('token'))

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
            form.add_error('username', gettext('Shop with this username already exists.'))
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


LANGUAGE_QUERY_PARAMETER = 'language'


def set_language(request):
    """
    Redirect to a given URL while setting the chosen language in the session
    (if enabled) and in a cookie. The URL and the language code need to be
    specified in the request parameters.
    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    next_url = '/'
    response = HttpResponseRedirect(next_url)
    if request.method == 'GET':
        lang_code = request.GET.get(LANGUAGE_QUERY_PARAMETER)
        if lang_code and check_for_language(lang_code):
            if next_url:
                next_trans = translate_url(next_url, lang_code)
                if next_trans != next_url:
                    response = HttpResponseRedirect(next_trans)
            if hasattr(request, 'session'):
                # Storing the language in the session is deprecated.
                # (RemovedInDjango40Warning)
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
                secure=settings.LANGUAGE_COOKIE_SECURE,
                httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                samesite=settings.LANGUAGE_COOKIE_SAMESITE,
            )
    return response
