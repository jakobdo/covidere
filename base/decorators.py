from functools import wraps

import tldextract
from django.shortcuts import redirect

from shop.models import Postcode


def postcode_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        valid_postcode = False
        url = request.build_absolute_uri()
        ext = tldextract.extract(url)
        if ext.subdomain:
            try:
                Postcode.objects.get(postcode=ext.subdomain)
                valid_postcode = True
            except Postcode.DoesNotExist:
                valid_postcode = False
        if valid_postcode:
             return function(request, *args, **kwargs)
        else:
            return redirect('postcode_index')
    return wrap
