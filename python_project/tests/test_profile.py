"""Module with tests for profile page."""

from django.contrib.auth.models import User
from django.test import TestCase

from python_project_app.models import Client, Discount

TESTUSER = 'testuser'
TESTPASSWORD = 'testpassword'


class ClientModelTests(TestCase):
    """
    Test case class for the Client model.

    Methods:
    setUp(self): Set up the test environment by creating a User and a Client instance.
    test_client_model_str(self): Test the string representation of the Client model.
    test_client_model_username(self): Test the username of the Client model.
    test_client_model_first_name(self): Test the first name of the Client model.
    test_client_model_last_name(self): Test the last name of the Client model.
    test_client_model_favorite_discounts(self): Test the functionality of adding favorite discount.
    """

    def setUp(self):
        """
        Set up the necessary objects before starting each test.

        - Creates a User instance with a specified username and password.
        - Creates a Client instance associated with the User.
        """
        self.user = User.objects.create_user(username=TESTUSER, password=TESTPASSWORD)
        self.client = Client.objects.create(user=self.user)

    def test_client_model_str(self):
        """Test the string representation of the Client model."""
        self.assertEqual(
            str(self.client),
            f'{self.client.user.username} ({self.client.user.first_name} {self.client.user.last_name})',
        )

    def test_client_model_username(self):
        """Test the username attribute of the Client model."""
        self.assertEqual(self.client.username, self.user.username)

    def test_client_model_first_name(self):
        """Test the first name attribute of the Client model."""
        self.assertEqual(self.client.first_name, self.user.first_name)

    def test_client_model_last_name(self):
        """Test the last name attribute of the Client model."""
        self.assertEqual(self.client.last_name, self.user.last_name)

    def test_client_model_favorite_discounts(self):
        """
        Test the functionality of adding favorite discounts to the Client model.

        - Creates a Discount instance.
        - Adds the Discount to the Client's favorite discounts.
        - Saves the Client and refreshes the instance from the database.
        - Checks if the Discount is in the Client's favorite discounts.
        """
        discount = Discount.objects.create(title='Test Discount')
        self.client.favorite_discounts.add(discount)
        self.client.save()
        self.client.refresh_from_db()
        self.assertIn(discount, self.client.favorite_discounts.all())
