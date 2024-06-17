"""Module with tests for forms."""

from django.test import TestCase

from python_project_app.forms import Registration

PASSWORD1 = 'password1'
PASSWORD2 = 'password2'


class TestRegistrationForm(TestCase):
    """
    Test case class for the Registration form.

    Attributes:
        _valid_attrs: Dictionary of valid attributes for form testing.
        _not_nullable_fields: Tuple of fields that cannot be empty in the form.

    Methods:
        test_empty(self): Test for checking empty fields in the form.
        test_invalid_email(self): Test for checking invalid email format.
        test_different_password(self): Test for checking when passwords are different.
        test_common_password(self): Test for checking if a common password is used.
        test_numeric_password(self): Test for checking if a numeric password is used.
        test_short_password(self): Test for checking if a short password is used.
        test_successfully_registered_user(self): Test for successfully registering a user.
    """

    _valid_attrs = {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        PASSWORD1: 'Gnkjhdfj8890',
        PASSWORD2: 'Gnkjhdfj8890',
        'email': 'sirius@sirius.ru',
    }
    _not_nullable_fields = ('username', PASSWORD1, PASSWORD2)

    def test_empty(self):
        """Test to check empty fields in the form."""
        for field in self._not_nullable_fields:
            attrs = self._valid_attrs.copy()
            attrs[field] = ''
            self.assertFalse(Registration(data=attrs).is_valid())

    def test_invalid_email(self):
        """Test to check invalid email format."""
        attrs = self._valid_attrs.copy()
        attrs['email'] = 'Vikusia'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_different_password(self):
        """Test to check when passwords are different."""
        attrs = self._valid_attrs.copy()
        attrs[PASSWORD1] = 'JHfdshkfdfkhs71239217'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_common_password(self):
        """Test to check if a common password is used."""
        attrs = self._valid_attrs.copy()
        attrs[PASSWORD1] = attrs[PASSWORD2] = 'Abcde123'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_numeric_password(self):
        """Test to check if a numeric password is used."""
        attrs = self._valid_attrs.copy()
        attrs[PASSWORD1] = attrs[PASSWORD2] = '123456789'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_short_password(self):
        """Test to check if a short password is used."""
        attrs = self._valid_attrs.copy()
        attrs[PASSWORD1] = attrs[PASSWORD2] = 'ABC123'
        self.assertFalse(Registration(data=attrs).is_valid())

    def test_successfully_registered_user(self):
        """Test for successfully registering a user."""
        self.assertTrue(Registration(data=self._valid_attrs).is_valid())
