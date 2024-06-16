from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from python_project_app.forms import Registration


class TestRegistrationForm(TestCase):
    _valid_attrs = {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'password1': 'Gnkjhdfj8890',
        'password2': 'Gnkjhdfj8890',
        'email': 'sirius@sirius.ru',
    }
    _not_nullable_fields = ('username', 'password1', 'password2')


    def test_empty(self):
        for field in self._not_nullable_fields:
            attrs = self._valid_attrs.copy()
            attrs[field] = ''
            self.assertFalse(Registration(data=attrs).is_valid())


    def test_invalid_email(self):
        attrs = self._valid_attrs.copy()
        attrs['email'] = 'Vadim Nikoforov'
        self.assertFalse(Registration(data=attrs).is_valid())


    def test_different_password(self):
        attrs = self._valid_attrs.copy()
        attrs['password1'] = 'JHfdshkfdfkhs71239217'
        self.assertFalse(Registration(data=attrs).is_valid())


    def test_common_password(self):
        attrs = self._valid_attrs.copy()
        attrs['password1'] = attrs['password2'] = 'Abcde123'
        self.assertFalse(Registration(data=attrs).is_valid())


    def test_numeric_password(self):
        attrs = self._valid_attrs.copy()
        attrs['password1'] = attrs['password2'] = '123456789'
        self.assertFalse(Registration(data=attrs).is_valid())


    def test_short_password(self):
        attrs = self._valid_attrs.copy()
        attrs['password1'] = attrs['password2'] = 'ABC123'
        self.assertFalse(Registration(data=attrs).is_valid())


    def test_successfully_registered_user(self):
        self.assertTrue(Registration(data=self._valid_attrs).is_valid())
