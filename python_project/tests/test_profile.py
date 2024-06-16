from django.contrib.auth.models import User
from django.test import TestCase

from python_project_app.models import Client, Discount


class ClientModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client.objects.create(user=self.user)

    def test_client_model_str(self):
        self.assertEqual(str(self.client), f'{self.client.user.username} ({self.client.user.first_name} {self.client.user.last_name})')

    def test_client_model_username(self):
        self.assertEqual(self.client.username, self.user.username)

    def test_client_model_first_name(self):
        self.assertEqual(self.client.first_name, self.user.first_name)

    def test_client_model_last_name(self):
        self.assertEqual(self.client.last_name, self.user.last_name)


    def test_client_model_favorite_discounts(self):
        discount = Discount.objects.create(title='Test Discount')
        self.client.favorite_discounts.add(discount)
        self.client.save()
        self.client.refresh_from_db()
        self.assertIn(discount, self.client.favorite_discounts.all())