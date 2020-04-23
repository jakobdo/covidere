from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand, CommandError

from base.models import User


class Command(BaseCommand):
    help = 'Create an alten admin user'

    def add_arguments(self, parser):
        parser.add_argument('alten_mail', help='Specifies the login for the alten admin user.')

    def handle(self, *args, **options):
        password = User.objects.make_random_password(length=14)
        
        username = options['alten_mail']
        try:
            user = User.objects.create_user(username, username, password)
            permission = Permission.objects.get(codename='alten_admin')
            user.user_permissions.add(permission)
            self.stdout.write(self.style.SUCCESS('Successfully created user'))
            self.stdout.write(self.style.SUCCESS('Username: %s' % username))
            self.stdout.write(self.style.SUCCESS('Password: %s' % password))
        except Exception as ex:
            raise CommandError(ex)
