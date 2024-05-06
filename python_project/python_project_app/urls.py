from django.urls import path, include
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
    path('discount/', views.discount_view, name='discount'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls), name='api'),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),

]