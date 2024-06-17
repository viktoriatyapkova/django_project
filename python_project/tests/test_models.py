"""Module with tests for models."""

from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from python_project_app import models

ABC = 'abc'
SHOP = 'shop'
MARKETPLACE = 'marketplace'
DISCOUNT = 'discount'
VALID_MIN_VALUE = float(0)
VALID_MAX_VALUE = 5.0
INVALID_MIN_VALUE = -1.0
INVALID_MAX_VALUE = 6.0
YEAR = 2022
DATE = 31
FALSE = False

valid_attrs = {
    MARKETPLACE: {'title': ABC, 'url_address': 'http://example.com'},
    SHOP: {'title': ABC, 'description': ABC, 'rating': 4.5},
    DISCOUNT: {
        'title': ABC,
        'description': ABC,
        'start_date': datetime(YEAR, 1, 1),
        'end_date': datetime(YEAR, 1, DATE),
    },
}


def create_model_tests(model_class, creation_attrs):
    """
    Create a test class for a specific model based on the provided creation attributes.

    Args:
        model_class: The Django model class for which the test class is being created.
        creation_attrs: Dictionary of attributes used for creating instances of the model.

    Returns:
        A dynamically created test class for the specified model.
    """
    class ModelTest(TestCase):
        def test_successful_creation(self):
            model_class.objects.create(**creation_attrs)

    return ModelTest


MarketplaceModelTest = create_model_tests(
    models.Marketplace, valid_attrs.get(MARKETPLACE),
)
ShopModelTest = create_model_tests(models.Shop, valid_attrs.get(SHOP))
DiscountModelTest = create_model_tests(models.Discount, valid_attrs.get(DISCOUNT))


class TestLinks(TestCase):
    """
    Test case class for testing links between different models.

    Methods:
        test_marketplaceshop(self): Test linking between marketplace and shop models.
        test_shopdiscount(self): Test linking between shop and discount models.
    """

    def test_marketplaceshop(self):
        """Test a marketplace and shop."""
        marketplace = models.Marketplace.objects.create(**valid_attrs.get(MARKETPLACE))
        shop = models.Shop.objects.create(**valid_attrs.get(SHOP))
        marketplace.shops.add(shop)
        marketplace.save()
        marketplaceshop_link = models.ShopToMarketplace.objects.filter(
            marketplace=marketplace, shop=shop,
        )
        self.assertEqual(len(marketplaceshop_link), 1)

    def test_shopdiscount(self):
        """Test a shop and a discount."""
        shop = models.Shop.objects.create(**valid_attrs.get(SHOP))
        discount = models.Discount.objects.create(
            shop=shop, **valid_attrs.get(DISCOUNT),
        )
        shopdiscount_link = models.Discount.objects.filter(
            shop=shop, title=discount.title,
        )
        self.assertEqual(len(shopdiscount_link), 1)


valid_rating_tests = (
    (models.MinValueValidator, VALID_MIN_VALUE),
    (models.MaxValueValidator, VALID_MAX_VALUE),
)
invalid_rating_tests = (
    (models.MinValueValidator, INVALID_MIN_VALUE),
    (models.MaxValueValidator, INVALID_MAX_VALUE),
)


def create_validation_test(validator, value, valid=True):
    """
    Create a validation test function for a given validator and value.

    Args:
        validator: The Django validator to be tested.
        value: The value to be validated.
        valid: A boolean indicating whether the value should pass validation.

    Returns:
        A test function that checks if the validator behaves as expected.
    """
    def test(self):
        with self.assertRaises(ValidationError):
            validator(value)

    return lambda _: validator(value) if valid else test


invalid_rating_methods = {
    f'test_invalid_rating_{args[0].__name__}': create_validation_test(*args, FALSE)
    for args in invalid_rating_tests
}
valid_rating_methods = {
    f'test_valid_rating_{args[0].__name__}': create_validation_test(*args)
    for args in valid_rating_tests
}
TestRatingValidators = type(
    'TestRatingValidators', (TestCase,), invalid_rating_methods | valid_rating_methods,
)
