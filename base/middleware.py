from postcode.models import Postcode


class PostcodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        code = request.GET.get('p')
        if code:
            try:
                postcode = Postcode.objects.get(postcode=code)
                request.session['postcode'] = dict(
                    code=postcode.postcode,
                    city=postcode.city
                )
            except Postcode.DoesNotExist:
                pass
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
