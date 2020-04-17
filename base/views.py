from django.conf import settings
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import Http404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext
from django.views.generic import FormView, TemplateView

from base.decorators import postcode_required
from base.models import User
from shop.forms import PostCodeForm
from shop.models import Postcode
from shop.tokens import account_activation_token


@method_decorator(postcode_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'


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
