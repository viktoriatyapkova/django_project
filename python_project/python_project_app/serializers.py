from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Discount, Marketplace, Shop


class ShopSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'id', 'title', 'description',
            'rating',
            'created', 'modified',
        ]

class MarketplaceSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Marketplace
        fields = [
            'id', 'title', 'url_address',
            'created', 'modified',
        ]

class DiscountSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'