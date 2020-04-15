from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import Http404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext
from django.views.generic import FormView, ListView, TemplateView

from base.models import User
from shop.forms import PostCodeForm
from shop.models import Postcode
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


class PostCodeView(FormView):
    template_name = 'base/postcode.html'
    form_class = PostCodeForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        response = super(PostCodeView, self).form_valid(form)
        response.set_cookie('postcode', form.cleaned_data.get('postcode'))
        return response


def postcodes(request):
    q = request.GET.get('q')
    try:
        code = Postcode.objects.get(postcode=q, active=True)
    except (Postcode.DoesNotExist, ValueError):
        return JsonResponse({'error': gettext("Postcode not found")}, status=400)
    return JsonResponse(dict(city=code.city))
