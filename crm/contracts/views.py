from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .forms import ContractForm
from .models import Contract
from crm.views_custom import CustomDeleteView, CustomCreateView, CustomUpdateView, PermissionsMixin
from products.models import Product


class ContractsListView(PermissionsMixin, ListView):
    template_name = "contracts/contracts-list.html"
    context_object_name = "contracts"
    queryset = Contract.objects.only("name")
    permission_required = "contracts.view_contract"


class ContractCreateView(PermissionsMixin, CustomCreateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-create.html"
    success_url = reverse_lazy("contracts:contracts-list")
    permission_required = "contracts.add_contract"


class ContractDeleteView(PermissionsMixin, CustomDeleteView):
    model = Contract
    template_name = "contracts/contracts-delete.html"
    success_url = reverse_lazy("contracts:contracts-list")
    permission_required = "contracts.delete_contract"


class ContractDetailView(PermissionsMixin, DetailView):
    template_name = "contracts/contracts-detail.html"
    product_qs = Product.objects.only("name")
    queryset = Contract.objects.prefetch_related((Prefetch("product", queryset=product_qs))).defer("created_by", "file")
    permission_required = "contracts.view_contract"


class ContractUpdateView(PermissionsMixin, CustomUpdateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-edit.html"
    permission_required = "contracts.change_contract"
