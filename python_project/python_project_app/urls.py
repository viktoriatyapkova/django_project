from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'shops', views.ShopViewSet)
router.register(r'marketplaces', views.MarketplaceViewSet)
router.register(r'discounts', views.DiscountViewSet)

urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('shops/', views.ShopListView.as_view(), name='shops'),
    path('shop/', views.shop_view, name='shop'),
    path('marketplaces/', views.MarketplaceListView.as_view(), name='marketplaces'),
    path('marketplace/', views.marketplace_view, name='marketplace'),
    path('discounts/', views.DiscountListView.as_view(), name='discounts'),
    path('discount/<uuid:discount_id>/', views.discount_detail, name='discount_detail'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls), name='api'),
    path('add/', views.add_to_favorites, name='add_to_favorites'),
    path('remove/<uuid:discount_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.favorites, name='favorites'),
    path('profile/', views.profile, name='profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)