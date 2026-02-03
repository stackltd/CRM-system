from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from crm.views_custom import (
    CustomCreateView,
    CustomDeleteView,
    CustomUpdateView,
    PermissionsMixin,
)

from .models import Product


class ProductsList(PermissionsMixin, ListView):
    """
    Список услуг
    """

    template_name = "products/products-list.html"
    queryset = Product.objects.only("name")
    context_object_name = "products"
    permission_required = "products.view_product"


class ProductCreateView(PermissionsMixin, CustomCreateView):
    """
    Создание услуги
    """

    model = Product
    template_name = "products/products-create.html"
    fields = ["name", "description", "cost"]
    success_url = reverse_lazy("products:products-list")
    permission_required = "products.add_product"


class ProductDeleteView(PermissionsMixin, CustomDeleteView):
    """
    Удаление услуги
    """

    model = Product
    template_name = "products/products-delete.html"
    success_url = reverse_lazy("products:products-list")
    permission_required = "products.delete_product"


class ProductDetailView(PermissionsMixin, DetailView):
    """
    Детализация услуги
    """

    template_name = "products/products-detail.html"
    model = Product
    permission_required = "products.view_product"


class ProductUpdateView(PermissionsMixin, CustomUpdateView):
    """
    Редактирование услуги
    """

    model = Product
    fields = ["name", "description", "cost"]
    template_name = "products/products-edit.html"
    permission_required = "products.change_product"
