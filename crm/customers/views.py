from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .models import Customer
from crm.views_custom import CustomDeleteView, CustomCreateView, CustomUpdateView


class CustomersListView(ListView):
    template_name = "customers/customers-list.html"
    context_object_name = "customers"
    queryset = Customer.objects.select_related("contract", "lead")


class CustomerCreateView(CustomCreateView):
    model = Customer
    fields = ["contract", "lead"]
    template_name = "customers/customers-create.html"
    success_url = reverse_lazy("customers:customers-list")


class CustomerDeleteView(CustomDeleteView):
    model = Customer
    template_name = "customers/customers-delete.html"
    success_url = reverse_lazy("customers:customers-list")


class CustomerDetailView(DetailView):
    template_name = "customers/customers-detail.html"
    queryset = Customer.objects.select_related("contract", "lead")


class CustomerUpdateView(CustomUpdateView):
    model = Customer
    fields = ["contract", "lead"]
    template_name = "customers/customers-edit.html"
