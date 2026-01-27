from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ContractForm
from .models import Contract

class ContractsListView(ListView):    
    template_name = "contracts/contracts-list.html"
    context_object_name = "contracts"
    queryset = Contract.objects.select_related("product")


class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-create.html"
    success_url = reverse_lazy("contracts:contracts-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save(commit=False)
        resp = super().form_valid(form)
        return resp


class ContractDeleteView(DeleteView):
    model = Contract
    template_name = "contracts/contracts-delete.html"
    success_url = reverse_lazy("contracts:contracts-list")


class ContractDetailView(DetailView):    
    template_name = "contracts/contracts-detail.html" # удалить, если имя шаблона в формате 'model_detail.html'
    queryset = Contract.objects.select_related("product")

# return obj.dateTo.strftime("%d-%m")

class ContractUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    # fields = ["product", "name", "start_date", "end_date", "cost", "file"]
    template_name = "contracts/contracts-edit.html"

    def get_success_url(self): # получаем ссылку на детализацию объекта, который был изменен и на который переходим после отправки формы изменения
        url = reverse("contracts:contracts-detail", kwargs={"pk": self.object.pk})
        return url

