from django.shortcuts import render
from django.views.generic import CreateView

from driver.models import Driver


class DriverRegisterView(CreateView):
    """
    Driver Register form.
    """
    model = Driver
    template_name = 'driver/register.html'
    form_class = DriverRegisterForm
    
    def get_success_url(self):
        return reverse('driver_registered')

    def form_valid(self, form):
        # Create a user, but remember to set inactive!
        user = User()
        user.username = form.cleaned_data.get('username')
        user.email = form.cleaned_data.get('username')
        user.set_password(form.cleaned_data.get('password'))
        user.is_active = False
        user.save()
        self.object = form.save(commit=False)
        self.object.user = user
        self.object.save()

        current_site = get_current_site(self.request)
        subject = gettext('Activate Your Account')
        message = render_to_string('emails/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        # TODO - Should also include readable plain text message
        user.email_user(subject, message='', html_message=message)
        return super().form_valid(form)


class DriverRegisteredView(TemplateView):
    template_name = 'driver/registered.html'
