from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Product
from crm.views_custom import CustomDeleteView, CustomCreateView, CustomUpdateView


class ProductsList(ListView):
    template_name = "products/products-list.html"
    model = Product
    context_object_name = "products"


class ProductCreateView(CustomCreateView):
    model = Product
    template_name = "products/products-create.html"
    fields = ["name", "description", "cost"]
    success_url = reverse_lazy("products:products-list")


class ProductDeleteView(CustomDeleteView):
    model = Product
    template_name = "products/products-delete.html"
    success_url = reverse_lazy("products:products-list")


class ProductDetailView(DetailView):
    template_name = "products/products-detail.html"
    model = Product


class ProductUpdateView(CustomUpdateView):
    model = Product
    fields = ["name", "description", "cost"]
    template_name = "products/products-edit.html"
