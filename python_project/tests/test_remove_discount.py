"""Module with tests for remove discounts from favorites."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from python_project_app.models import Client as ModelClient
from python_project_app.models import Discount

TESTUSER = 'testuser'
TESTPASSWORD = 'testpassword'


class FavoritesViewTests(TestCase):
    """
    Test case class for testing views related to favorite discounts.

    Methods:
    setUp(self): Set up the necessary test environment by creating a user.
    test_remove_from_favorites_view_loads(self): Test whether the 'remove_from_favorites'.

    """

    def setUp(self):
        """
        Set up the necessary objects before starting each test.

        - Creates a test client.
        - Creates a User instance with a specific username and password.
        - Logs in the client as the created user.
        - Creates a ModelClient instance associated with the user.
        - Creates a Discount instance.
        """
        self.client = Client()
        self.user = User.objects.create_user(username=TESTUSER, password=TESTPASSWORD)
        self.client.force_login(self.user)
        self.client_profile = ModelClient.objects.create(user=self.user)
        self.discount = Discount.objects.create(title='Test Discount')

    def test_remove_from_favorites_view_loads(self):
        """
        Test whether the 'remove_from_favorites' view loads properly upon accessing it.

        - Adds a discount to the favorite discounts of the client profile.
        - Saves the client profile.
        - Sends a get request to the 'remove_from_favorites' view with the discount id.
        - Validates the response.
        """
        self.client_profile.favorite_discounts.add(self.discount)
        self.client_profile.save()
        self.assertEqual
