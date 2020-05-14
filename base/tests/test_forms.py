import pytest

from base.forms import SetUsernameAndPasswordForm


class TestSetUsernameAndPasswordForm:
    form = SetUsernameAndPasswordForm

    @pytest.mark.parametrize(
        'username, password1, password2, validity',
        [
            ('username', 'Abcd!2345', 'Abcd!2345', True),
            (None, 'Abcd!2345', 'Abcd!2345', False),
            ('username', 'Abcd!5432', 'Abcd!2345', False),
            ('username', 'Abcd!2345', 'Abcd!5432', False),
        ]
    )
    def test_set_username_password_form(self, user, username, password1, password2, validity):
        form = self.form(user=user, data={
            'username': username,
            'password1': password1,
            'password2': password2
        })
        result = form.is_valid()
        assert result is validity
