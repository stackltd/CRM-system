from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .forms import ContractForm
from .models import Contract
from crm.views_custom import CustomDeleteView, CustomCreateView, CustomUpdateView


class ContractsListView(ListView):
    template_name = "contracts/contracts-list.html"
    context_object_name = "contracts"
    queryset = Contract.objects.select_related("product")


class ContractCreateView(CustomCreateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-create.html"
    success_url = reverse_lazy("contracts:contracts-list")


class ContractDeleteView(CustomDeleteView):
    model = Contract
    template_name = "contracts/contracts-delete.html"
    success_url = reverse_lazy("contracts:contracts-list")


class ContractDetailView(DetailView):
    template_name = "contracts/contracts-detail.html"
    queryset = Contract.objects.select_related("product")


class ContractUpdateView(CustomUpdateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-edit.html"
