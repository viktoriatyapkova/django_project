"""Module with test for API."""

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from python_project_app.models import Discount, Marketplace, Shop

ABC = 'abc'
ADMIN = 'admin'


def create_api_test(model, url, creation_attrs):
    """
    Create a test class for the given model API endpoints.

    Args:
        model: The Django model for which the API test class is being created.
        url: The base URL of the API endpoint for the given model.
        creation_attrs: The attributes used for creating instances when testing the API.

    Returns:
        Сreate test class that includes test methods for API operations base on the provided model.
    """
    class ApiTest(TestCase):
        def setUp(self) -> None:
            self.client = APIClient()
            self.user = User.objects.create(username=ABC, password=ABC)
            self.superuser = User.objects.create(
                username=ADMIN,
                password=ADMIN,
                is_superuser=True,
            )
            self.user_token = Token(user=self.user)
            self.superuser_token = Token(user=self.superuser)

        def manage(
            self,
            user: User,
            token: Token,
            post_expected: int,
            put_expected: int,
            delete_expected: int,
        ):
            self.client.force_authenticate(user=user, token=token)

            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.head(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.options(url).status_code, status.HTTP_200_OK)

            self.assertEqual(
                self.client.post(url, creation_attrs).status_code, post_expected,
            )

            created_id = model.objects.create(**creation_attrs).id
            instance_url = f'{url}{created_id}/'
            put_response = self.client.put(instance_url, creation_attrs)
            self.assertEqual(put_response.status_code, put_expected)

            delete_response = self.client.delete(instance_url, creation_attrs)
            self.assertEqual(delete_response.status_code, delete_expected)

        def test_superuser(self):
            self.manage(
                self.superuser,
                self.superuser_token,
                post_expected=status.HTTP_201_CREATED,
                put_expected=status.HTTP_200_OK,
                delete_expected=status.HTTP_204_NO_CONTENT,
            )

        def test_user(self):
            self.manage(
                self.user,
                self.user_token,
                post_expected=status.HTTP_403_FORBIDDEN,
                put_expected=status.HTTP_403_FORBIDDEN,
                delete_expected=status.HTTP_403_FORBIDDEN,
            )

    return ApiTest


url = '/api/'
MarketplaceAuthorApiTest = create_api_test(
    Marketplace, f'{url}marketplaces/', {'title': 'test marketplace'},
)
ShopApiTest = create_api_test(Shop, f'{url}shops/', {'title': 'test shop'})
DiscountApiTest = create_api_test(Discount, f'{url}discounts/', {'title': 'test_title'})
