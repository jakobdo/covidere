from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import gettext
from django.views.generic import FormView

from postcode.forms import PostCodeForm
from postcode.models import Postcode


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
