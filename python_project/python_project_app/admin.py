from django.contrib import admin
from .models import Shop, Marketplace, ShopToMarketplace, Discount


class ShopToMarketplaceInline(admin.TabularInline):
    model = ShopToMarketplace
    extra = 1
    
class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 1


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'rating')
    inlines = (DiscountInline, ShopToMarketplaceInline)
    search_fields = ('title', 'description')
    list_filter = ('title', 'rating')
    
@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_address')
    inlines = (ShopToMarketplaceInline, )
    search_fields = ('title',)
    list_filter = ('title', )

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    list_filter = ('title', 'start_date', 'end_date')

admin.site.register(ShopToMarketplace)  
