"""Module with views."""

from typing import Any

from django.contrib import messages
from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from rest_framework import authentication, permissions, viewsets

from .forms import Registration
from .models import Client, Discount, Marketplace, Shop
from .serializers import DiscountSerializer, MarketplaceSerializer, ShopSerializer


def home_page(request):
    """
    Render the home page with counts of shops, marketplaces, and discounts.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered response for the home page.
    """
    return render(
        request,
        'index.html',
        {
            'shops': Shop.objects.count(),
            'marketplaces': Marketplace.objects.count(),
            'discounts': Discount.objects.count(),
        },
    )


def create_list_view(model_class, plural_name, template):
    """
    Create a custom ListView for the provided model class.

    Args:
        model_class: The model class to create the view for.
        plural_name: The plural name to use in the context.
        template: The template path for rendering the view.

    Returns:
        Custom ListView class for the model.

    """

    class CustomListView(mixins.LoginRequiredMixin, ListView):
        """
        Custom ListView class for a model.

        Attributes:
            model: The model class used in the view.
            template_name: The template path for rendering the view.
            paginate_by: Number of objects per page.
            context_object_name: The context object name for the queryset.

        Methods:
            get_context_data(): Get the context data for the view.

        """

        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            ob = model_class.objects.all()
            paginator = Paginator(ob, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context

    return CustomListView


ShopListView = create_list_view(Shop, 'shops', 'catalog/shops.html')
MarketplaceListView = create_list_view(
    Marketplace,
    'marketplaces',
    'catalog/marketplaces.html',
)
DiscountListView = create_list_view(Discount, 'discounts', 'catalog/discounts.html')


def create_view(model_class, context_name, template):
    """
    Create a custom detail view for the provided model class.

    Args:
        model_class: The model class to create the view for.
        context_name: The context name for the object.
        template: The template path for rendering the view.

    Returns:
        Custom detail view function for the model.

    """

    def view(request):
        """
        Retrieve an object of a specific model based on the request parameter.

        Args:
            request: The HTTP request object containing parameters.

        Returns:
            Rendered response with the specified object in the provided template context.
        """
        id_ = request.GET.get('id', None)
        target = model_class.objects.get(id=id_) if id_ else None
        return render(request, template, {context_name: target})

    return view


shop_view = create_view(Shop, 'shop', 'entities/shop.html')
discount_view = create_view(Discount, 'discount', 'entities/discount.html')
marketplace_view = create_view(Marketplace, 'marketplace', 'entities/marketplace.html')


def register(request):
    """
    Handle user registration form submission.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered response for the registration page with form and errors if any.

    """
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
        },
    )


class MyPermission(permissions.BasePermission):
    """
    Custom permission class for handling permissions based on user roles.

    Attributes:
        _safe_methods: Tuple of safe HTTP methods.
        _unsafe_methods: Tuple of unsafe HTTP methods.

    Methods:
        has_permission(self, request, _): Check if the user has permission for the request.

    """

    _safe_methods = 'GET', 'HEAD', 'OPTIONS'
    _unsafe_methods = 'POST', 'PUT', 'DELETE', 'PATCH'

    def has_permission(self, request, _):
        """
        Check if the user has permission for the given request.

        Args:
            request: The HTTP request object.
            _: Not used in this function, kept for compatibility with Django permissions.

        Returns:
            True if the user has permission for the request, False otherwise.
        """
        if request.method in self._safe_methods and (
            request.user and request.user.is_authenticated
        ):
            return True
        if request.method in self._unsafe_methods and (
            request.user and request.user.is_superuser
        ):
            return True
        return False


def create_viewset(model_class, serializer):
    """
    Create a custom ViewSet for the provided model class.

    Args:
        model_class: The model class to create the ViewSet for.
        serializer: The serializer class to use for serializing data.

    Returns:
        Custom ModelViewSet class for the model.

    """

    class CustomViewSet(viewsets.ModelViewSet):
        serializer_class = serializer
        queryset = model_class.objects.all()
        permission_classes = [MyPermission]
        authentication_classes = [authentication.TokenAuthentication]

    return CustomViewSet


ShopViewSet = create_viewset(Shop, ShopSerializer)
MarketplaceViewSet = create_viewset(Marketplace, MarketplaceSerializer)
DiscountViewSet = create_viewset(Discount, DiscountSerializer)


@login_required
def add_to_favorites(request):
    """
    Add a discount to the user's list of favorite discounts.

    Args:
        request: The HTTP request object containing discount ID.

    Returns:
        Redirects to the favorites page after adding the discount to favorites.
    """
    discount_id = request.GET.get('id')
    if not discount_id:
        messages.error(request, 'Discount ID is missing.')
        return redirect('discount_list')

    try:
        discount = get_object_or_404(Discount, id=discount_id)
        user = request.user

        client, _ = Client.objects.get_or_create(user=user)

        if discount not in client.favorite_discounts.all():
            client.favorite_discounts.add(discount)
            messages.success(request, 'Discount added to favorites.')
        else:
            messages.info(request, 'This discount is already in your favorites.')
    except Exception as exc:
        messages.error(request, f'An error occurred: {exc}')
        return redirect('discount_list')

    return redirect('favorites')


@login_required
def remove_from_favorites(request, discount_id):
    """
    Remove a discount from the user's list of favorite discounts.

    Args:
        request: The HTTP request object.
        discount_id: The ID of the discount to be removed.

    Returns:
        Redirects to the favorites page after removing the discount from favorites.
    """
    discount = get_object_or_404(Discount, id=discount_id)
    user = request.user

    try:
        client = Client.objects.get(user=user)

        if discount in client.favorite_discounts.all():
            client.favorite_discounts.remove(discount)
            messages.success(request, 'Discount removed from favorites.')
        else:
            messages.warning(request, 'This discount is not in your favorites.')
    except Client.DoesNotExist:
        messages.error(request, 'Client account does not exist.')
    except Exception as exc:
        messages.error(request, f'An error occurred: {exc}')

    return redirect('favorites')


@login_required
def favorites(request):
    """
    Display the user's favorite discounts.

    Args:
        request: The HTTP request object.

    Returns:
        Renders the favorites page with the user's favorite discounts.
    """
    user = request.user

    try:
        client = Client.objects.get(user=user)
        discounts = client.favorite_discounts.all()
    except Client.DoesNotExist:
        discounts = []
        messages.error(request, 'Client account does not exist.')
    except Exception as exc:
        discounts = []
        messages.error(request, f'An error occurred: {exc}')

    return render(request, 'catalog/favorites.html', {'discounts': discounts})


@login_required
def discount_detail(request, discount_id):
    """
    Display details of a specific discount.

    Args:
        request: The HTTP request object.
        discount_id: The ID of the discount to display details for.

    Returns:
        Renders the discount detail page with the specified discount details.
    """
    discount = get_object_or_404(Discount, id=discount_id)
    user = request.user

    try:
        client = Client.objects.get(user=user)
        favorite_discounts = client.favorite_discounts.all()
    except Client.DoesNotExist:
        favorite_discounts = []

    return render(
        request,
        'entities/discount.html',
        {
            'discount': discount,
            'user': user,
            'favorite_discounts': favorite_discounts,
        },
    )


@login_required
def profile(request):
    """
    Display and allow editing of the user's profile information.

    Args:
        request: The HTTP request object.

    Returns:
        Renders the profile page with user's profile information and allows editing.
    """
    client = Client.objects.get(user=request.user)

    if request.method == 'POST':
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            client.photo = photo
            client.save()

    return render(
        request,
        'pages/profile.html',
        {'client_profile': client},
    )
