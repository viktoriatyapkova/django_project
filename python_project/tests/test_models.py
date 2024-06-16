from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _

from python_project_app import models

valid_attrs = {
    'marketplace': {'title': 'ABC', 'url_address': 'http://example.com'},
    'shop': {'title': 'ABC', 'description': 'ABC', 'rating': 4.5},
    'discount': {'title': 'ABC', 'description': 'ABC', 'start_date': datetime(2022, 1, 1), 'end_date': datetime(2022, 1, 31)},
}

def create_model_tests(model_class, creation_attrs):
    class ModelTest(TestCase):
        def test_successful_creation(self):
            model_class.objects.create(**creation_attrs)
    return ModelTest

MarketplaceModelTest = create_model_tests(models.Marketplace, valid_attrs.get('marketplace'))
ShopModelTest = create_model_tests(models.Shop, valid_attrs.get('shop'))
DiscountModelTest = create_model_tests(models.Discount, valid_attrs.get('discount'))

class TestLinks(TestCase):
    def test_marketplaceshop(self):
        marketplace = models.Marketplace.objects.create(**valid_attrs.get('marketplace'))
        shop = models.Shop.objects.create(**valid_attrs.get('shop'))
        marketplace.shops.add(shop)
        marketplace.save()
        marketplaceshop_link = models.ShopToMarketplace.objects.filter(marketplace=marketplace, shop=shop)
        self.assertEqual(len(marketplaceshop_link), 1)

    def test_shopdiscount(self):
        shop = models.Shop.objects.create(**valid_attrs.get('shop'))
        discount = models.Discount.objects.create(shop=shop, **valid_attrs.get('discount'))
        shopdiscount_link = models.Discount.objects.filter(shop=shop, title=discount.title)
        self.assertEqual(len(shopdiscount_link), 1)

valid_rating_tests = (
    (models.MinValueValidator, 0.0),
    (models.MaxValueValidator, 5.0),
)
invalid_rating_tests = (
    (models.MinValueValidator, -1.0),
    (models.MaxValueValidator, 6.0),
)


def create_validation_test(validator, value, valid=True):
    def test(self):
        with self.assertRaises(ValidationError):
            validator(value)
    return lambda _: validator(value) if valid else test


invalid_rating_methods = {
    f'test_invalid_rating_{args[0].__name__}': create_validation_test(*args, False) for args in invalid_rating_tests
}
valid_rating_methods = {
    f'test_valid_rating_{args[0].__name__}': create_validation_test(*args) for args in valid_rating_tests
}
TestRatingValidators = type('TestRatingValidators', (TestCase,), invalid_rating_methods | valid_rating_methods)
        


