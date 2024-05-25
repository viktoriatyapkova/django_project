from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib.auth import mixins
from rest_framework import viewsets, permissions, authentication
from typing import Any

from .models import Shop, Marketplace, Discount, Client
from .forms import Registration
from .serializers import ShopSerializer, MarketplaceSerializer, DiscountSerializer

def home_page(request):
    return render(
        request,
        'index.html',
        {
            'shops': Shop.objects.count(),
            'marketplaces': Marketplace.objects.count(),
            'discounts': Discount.objects.count(),
        }
    )

def create_list_view(model_class, plural_name, template):
    class CustomListView(mixins.LoginRequiredMixin, ListView):
        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            obj = model_class.objects.all()
            paginator = Paginator(obj, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context
    return CustomListView

ShopListView = create_list_view(Shop, 'shops', 'catalog/shops.html')
MarketplaceListView = create_list_view(Marketplace, 'marketplaces', 'catalog/marketplaces.html')
DiscountListView = create_list_view(Discount, 'discounts', 'catalog/discounts.html')

def create_view(model_class, context_name, template):
    def view(request):
        id_ = request.GET.get('id', None)
        target = model_class.objects.get(id=id_) if id_ else None
        return render(request, template, {context_name: target})
    return view


shop_view = create_view(Shop, 'shop', 'entities/shop.html')
discount_view = create_view(Discount, 'discount', 'entities/discount.html')
marketplace_view = create_view(Marketplace, 'marketplace', 'entities/marketplace.html')

def register(request):
    errors = ''
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
        else:
            errors = form.errors
    else:
        form = Registration()

    return render(
        request,
        'registration/register.html',
        {
            'form': form,
            'errors': errors,
        }
    )

class MyPermission(permissions.BasePermission):
    _safe_methods = 'GET', 'HEAD', 'OPTIONS' 
    _unsafe_methods = 'POST', 'PUT', 'DELETE', 'PATCH'

    def has_permission(self, request, _):
        if request.method in self._safe_methods and (request.user and request.user.is_authenticated):
            return True
        if request.method in self._unsafe_methods and (request.user and request.user.is_superuser):
            return True
        return False

def create_viewset(model_class, serializer):
    class CustomViewSet(viewsets.ModelViewSet):
        serializer_class = serializer
        queryset = model_class.objects.all()
        permission_classes = [MyPermission]
        authentication_classes = [authentication.TokenAuthentication]

    return CustomViewSet

ShopViewSet = create_viewset(Shop, ShopSerializer)
MarketplaceViewSet = create_viewset(Marketplace, MarketplaceSerializer)
DiscountViewSet = create_viewset(Discount, DiscountSerializer)
