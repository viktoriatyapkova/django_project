"""Module with serializers."""

from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Discount, Marketplace, Shop


class ShopSerializer(HyperlinkedModelSerializer):
    """Serializer for the Shop model."""

    class Meta:
        """Metadata class for the ShopSerializer."""

        model = Shop
        fields = [
            'id',
            'title',
            'description',
            'rating',
            'created',
            'modified',
        ]


class MarketplaceSerializer(HyperlinkedModelSerializer):
    """Serializer for the Marketplace model."""

    class Meta:
        """Metadata class for the MarketplaceSerializer."""

        model = Marketplace
        fields = [
            'id',
            'title',
            'url_address',
            'created',
            'modified',
        ]


class DiscountSerializer(HyperlinkedModelSerializer):
    """Serializer for the Discount model."""

    class Meta:
        """Metadata class for the DiscountSerializer."""

        model = Discount
        fields = '__all__'
