from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .models import Customer
from crm.views_custom import CustomDeleteView, CustomCreateView, CustomUpdateView, PermissionsMixin
from leads.models import Lead


class CustomersListView(PermissionsMixin, ListView):
    template_name = "customers/customers-list.html"
    context_object_name = "customers"
    lead_qs = Lead.objects.only("first_name", "last_name")
    queryset = Customer.objects.prefetch_related((Prefetch("lead", queryset=lead_qs))).defer("created_by")
    permission_required = "customers.view_customer"


class CustomerCreateView(PermissionsMixin, CustomCreateView):
    model = Customer
    fields = ["contract", "lead"]
    template_name = "customers/customers-create.html"
    success_url = reverse_lazy("customers:customers-list")
    permission_required = "customers.add_customer"


class CustomerDeleteView(PermissionsMixin, CustomDeleteView):
    model = Customer
    template_name = "customers/customers-delete.html"
    success_url = reverse_lazy("customers:customers-list")
    permission_required = "customers.delete_customer"


class CustomerDetailView(PermissionsMixin, DetailView):
    template_name = "customers/customers-detail.html"
    lead_qs = Lead.objects.defer("created_by")
    queryset = Customer.objects.prefetch_related((Prefetch("lead", queryset=lead_qs))).defer("created_by")
    permission_required = "customers.view_customer"


class CustomerUpdateView(PermissionsMixin, CustomUpdateView):
    model = Customer
    fields = ["contract", "lead"]
    template_name = "customers/customers-edit.html"
    permission_required = "customers.change_customer"
