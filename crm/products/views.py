from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Product

class ProductsList(ListView):
    template_name = "products/products-list.html"
    model = Product
    context_object_name = "products"


class ProductCreateView(CreateView):
    model = Product
    template_name = "products/products-create.html"
    fields = ["name", "description", "cost"]
    success_url = reverse_lazy("products:products-list")

    def form_valid(self, form):
        # получение user и сохранение created_by для Product
        form.instance.created_by = self.request.user
        form.save(commit=False)
        resp = super().form_valid(form)
        return resp


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/products-delete.html"
    success_url = reverse_lazy("products:products-list")


class ProductDetailView(DetailView):    
    template_name = "products/products-detail.html"
    model = Product


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "description", "cost"]
    template_name = "products/products-edit.html"

    def get_success_url(self):
        url = reverse("products:product-detail", kwargs={"pk": self.object.pk})
        return url
