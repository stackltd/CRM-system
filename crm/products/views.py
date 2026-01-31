from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Product
from crm.views_custom import CustomDeleteView, CustomCreateView, CustomUpdateView, PermissionsMixin


class ProductsList(PermissionsMixin, ListView):
    template_name = "products/products-list.html"
    queryset = Product.objects.only("name")
    context_object_name = "products"
    permission_required = "products.view_product"


class ProductCreateView(PermissionsMixin, CustomCreateView):
    model = Product
    template_name = "products/products-create.html"
    fields = ["name", "description", "cost"]
    success_url = reverse_lazy("products:products-list")
    permission_required = "products.add_product"


class ProductDeleteView(PermissionsMixin, CustomDeleteView):
    model = Product
    template_name = "products/products-delete.html"
    success_url = reverse_lazy("products:products-list")
    permission_required = "products.delete_product"


class ProductDetailView(PermissionsMixin, DetailView):
    template_name = "products/products-detail.html"
    model = Product
    permission_required = "products.view_product"


class ProductUpdateView(PermissionsMixin, CustomUpdateView):
    model = Product
    fields = ["name", "description", "cost"]
    template_name = "products/products-edit.html"
    permission_required = "products.change_product"
