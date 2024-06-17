"""Model with tests for views."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from python_project_app.models import Client as ClientModel

USER = 'user'
PASSWORD = 'password'


def create_successful_page_test(page_url, page_name, template, auth=True):
    """
    Create a test function for a successful page load.

    Args:
        page_url: The URL of the page to test.
        page_name: The name of the page for testing purposes.
        template: The template expected to be used by the page.
        auth: A boolean indicating whether authentication is required for access.

    Returns:
        test function: The created test function.
    """
    def test(self):
        self.client = Client()
        if auth:
            user = User.objects.create_user(username=USER, password=PASSWORD)
            ClientModel.objects.create(user=user)
            self.client.force_login(user)

        url = page_url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, template)

    return test


def create_redirect_page_test(page_name):
    """
    Create a test function for a page that should redirect.

    Args:
        page_name: The name of the page for testing redirection.

    Returns:
        test function: The created test function.
    """
    def test(self):
        self.client = Client()
        self.client.logout()
        self.assertEqual(self.client.get(reverse(page_name)).status_code, status.HTTP_302_FOUND)

    return test


auth_pages = (
    ('/favorites/', 'add_to_favorites', 'catalog/favorites.html'),
    ('/shops/', 'shops', 'catalog/shops.html'),
    ('/marketplaces/', 'marketplaces', 'catalog/marketplaces.html'),
    ('/discounts/', 'discounts', 'catalog/discounts.html'),
    ('/shop/', 'shop', 'entities/shop.html'),
    ('/marketplace/', 'marketplace', 'entities/marketplace.html'),
)

casual_pages = (
    ('/register/', 'register', 'registration/register.html'),
    ('', 'homepage', 'index.html'),
    ('/accounts/login/', 'login', 'registration/login.html'),
)

casual_methods = {f'test_{page[1]}': create_successful_page_test(*page) for page in casual_pages}
TestCasualPages = type('TestCasualPages', (TestCase,), casual_methods)

auth_pages_methods = {f'test_{page[1]}': create_successful_page_test(*page) for page in auth_pages}
TestAuthPages = type('TestAuthPages', (TestCase,), auth_pages_methods)
