from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from python_project_app.models import Client as ModelClient
from python_project_app.models import Discount


class FavoritesViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.client_profile = ModelClient.objects.create(user=self.user)
        self.discount = Discount.objects.create(title='Test Discount')


    def test_remove_from_favorites_view_loads(self):
        self.client_profile.favorite_discounts.add(self.discount)
        self.client_profile.save()
        response = self.client.get(reverse('remove_from_favorites', args=[self.discount.id]))
        self.assertEqual