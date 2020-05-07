from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext
from django.views import View

from postcode.forms import PostCodeForm
from postcode.models import Postcode


class PostCodeView(View):
    def post(self, request, *args, **kwargs):
        form = PostCodeForm(request.POST)
        if form.is_valid():
            postcode = form.cleaned_data.get('postcode')
            return redirect('products_postcode', postcode=postcode.postcode)
        return redirect('index')


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
