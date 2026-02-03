from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from crm.views_custom import (
    CustomCreateView,
    CustomDeleteView,
    CustomUpdateView,
    PermissionsMixin,
)
from products.models import Product

from .forms import ContractForm
from .models import Contract


class ContractsListView(PermissionsMixin, ListView):
    """
    Список услуг
    """

    template_name = "contracts/contracts-list.html"
    context_object_name = "contracts"
    queryset = Contract.objects.only("name")
    permission_required = "contracts.view_contract"


class ContractCreateView(PermissionsMixin, CustomCreateView):
    """
    Создание услуги
    """

    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-create.html"
    success_url = reverse_lazy("contracts:contracts-list")
    permission_required = "contracts.add_contract"


class ContractDeleteView(PermissionsMixin, CustomDeleteView):
    """
    Удаление услуги
    """

    model = Contract
    template_name = "contracts/contracts-delete.html"
    success_url = reverse_lazy("contracts:contracts-list")
    permission_required = "contracts.delete_contract"


class ContractDetailView(PermissionsMixin, DetailView):
    """
    Детализация услуги
    """

    template_name = "contracts/contracts-detail.html"
    product_qs = Product.objects.only("name")
    queryset = Contract.objects.prefetch_related(
        (Prefetch("product", queryset=product_qs))
    ).defer("created_by", "file")
    permission_required = "contracts.view_contract"


class ContractUpdateView(PermissionsMixin, CustomUpdateView):
    """
    Обновление услуги
    """

    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-edit.html"
    permission_required = "contracts.change_contract"
