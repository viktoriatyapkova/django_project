"""Module with admin."""

from django.contrib import admin

from .models import Discount, Marketplace, Shop, ShopToMarketplace


class ShopToMarketplaceInline(admin.TabularInline):
    """
    Inline class for the ShopToMarketplace model.

    Attributes:
        model (Model): The model to be displayed in the inline.
        extra (int): The number of extra forms to be displayed.
    """

    model = ShopToMarketplace
    extra = 1


class DiscountInline(admin.TabularInline):
    """
    Inline class for the Discount model.

    Attributes:
        model (Model): The model to be displayed in the inline.
        extra (int): The number of extra forms to be displayed.
    """

    model = Discount
    extra = 1


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """
    Admin interface for the Shop model.

    Attributes:
        list_display (tuple): A tuple of field names to display in the list view.
        inlines (tuple): A tuple of inline classes to include in the admin interface.
        search_fields (tuple): A tuple of field names to enable searching by.
        list_filter (tuple): A tuple of field names to enable filtering by.
    """

    list_display = ('title', 'description', 'rating')
    inlines = (DiscountInline, ShopToMarketplaceInline)
    search_fields = ('title', 'description')
    list_filter = ('title', 'rating')


@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    """
    Admin interface for the Marketplace model.

    Attributes:
        list_display (tuple): A tuple of field names to display in the list view.
        inlines (tuple): A tuple of inline classes to include in the admin interface.
        search_fields (tuple): A tuple of field names to enable searching by.
        list_filter (tuple): A tuple of field names to enable filtering by.
    """

    list_display = ('title', 'url_address')
    inlines = (ShopToMarketplaceInline, )
    search_fields = ('title',)
    list_filter = ('title', )


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """
    Admin interface for the Discount model.

    Attributes:
        list_display (tuple): A tuple of field names to display in the list view.
        search_fields (tuple): A tuple of field names to enable searching by.
        list_filter (tuple): A tuple of field names to enable filtering by.
    """

    list_display = ('title', 'description', 'start_date', 'end_date', 'image')
    search_fields = ('title', 'description')
    list_filter = ('title', 'start_date', 'end_date')


admin.site.register(ShopToMarketplace)
