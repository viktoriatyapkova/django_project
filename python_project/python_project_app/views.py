from typing import Any

from django.contrib import messages
from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from rest_framework import authentication, permissions, viewsets

from .forms import AddShopForm, ProfilePhotoForm, Registration
from .models import Client, Discount, FavoriteDiscount, Marketplace, Shop
from .serializers import (DiscountSerializer, MarketplaceSerializer,
                          ShopSerializer)


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



from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Client, Discount


@login_required
def add_to_favorites(request):
    discount_id = request.GET.get('id')
    if not discount_id:
        messages.error(request, "Discount ID is missing.")
        return redirect('discount_list')
    
    try:
        discount = get_object_or_404(Discount, id=discount_id)
        user = request.user

        client, created = Client.objects.get_or_create(user=user)

        if discount not in client.favorite_discounts.all():
            client.favorite_discounts.add(discount)
            messages.success(request, "Discount added to favorites.")
        else:
            messages.info(request, "This discount is already in your favorites.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('discount_list')

    return redirect('favorites')

@login_required
def remove_from_favorites(request, discount_id):
    discount = get_object_or_404(Discount, id=discount_id)
    user = request.user
    
    try:
        client = Client.objects.get(user=user)

        if discount in client.favorite_discounts.all():
            client.favorite_discounts.remove(discount)
            messages.success(request, "Discount removed from favorites.")
        else:
            messages.warning(request, "This discount is not in your favorites.")
    except Client.DoesNotExist:
        messages.error(request, "Client account does not exist.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")

    return redirect('favorites')

@login_required
def favorites(request):
    user = request.user
    
    try:
        client = Client.objects.get(user=user)
        discounts = client.favorite_discounts.all()
    except Client.DoesNotExist:
        discounts = []
        messages.error(request, "Client account does not exist.")
    except Exception as e:
        discounts = []
        messages.error(request, f"An error occurred: {e}")
      
    return render(request, 'catalog/favorites.html', {'discounts': discounts})


@login_required
def discount_detail(request, discount_id):
    discount = get_object_or_404(Discount, id=discount_id)
    user = request.user
    
    try:
        client = Client.objects.get(user=user)
        favorite_discounts = client.favorite_discounts.all()
    except Client.DoesNotExist:
        favorite_discounts = []

    return render(request, 'entities/discount.html', {
        'discount': discount,
        'user': user,
        'favorite_discounts': favorite_discounts
    })
    

@login_required
def profile(request):
    client = Client.objects.get(user=request.user)
    
    photo_form_errors = ''

    if request.method == 'POST':
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            client.photo = photo
            client.save()
        else:
            photo_form_errors = 'Please select a photo to upload!'
    else:
        pass  # No need to do anything on GET requests

    client_attrs = ('username', 'first_name', 'last_name')
    client_data = {attr: getattr(client, attr) for attr in client_attrs}
    return render(
        request,
        'pages/profile.html',
        {'client_profile': client},
    ) 