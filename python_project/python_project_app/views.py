from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from typing import Any


from .models import Shop, Marketplace, Discount

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
    class ModelListView(ListView):
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
    return ModelListView

Shop_ListView = create_list_view(Shop, 'shops', 'catalog/shops.html')
Marketplace_ListView = create_list_view(Marketplace, 'marketplaces', 'catalog/marketplaces.html')
Discount_ListView = create_list_view(Discount, 'discounts', 'catalog/discounts.html')

def create_view(model_class, context_name, template):
    def view(request):
        id_ = request.GET.get('id', None)
        target = model_class.objects.get(id=id_) if id_ else None
        return render(request, template, {context_name: target})
    return view


Shop_ListView = create_list_view(Shop, 'shops', 'catalog/shops.html')
Discount_ListView = create_list_view(Discount, 'discounts', 'catalog/discounts.html')
Marketplace_ListView = create_list_view(Marketplace, 'marketplaces', 'catalog/marketplaces.html')

shop_view = create_view(Shop, 'shop', 'entities/shop.html')
subtype_view = create_view(Discount, 'discount', 'entities/discount.html')
manufacturer_view = create_view(Marketplace, 'marketplace', 'entities/marketplace.html')
