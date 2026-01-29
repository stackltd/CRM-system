from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Lead
from ads.models import Ad
from crm.views_custom import CustomDeleteView, CustomCreateView, CustomUpdateView


class LeadsListView(ListView):
    template_name = "leads/leads-list.html"
    context_object_name = "leads"
    queryset = Lead.objects.select_related("ad")


class LeadCreateView(CustomCreateView):
    model = Lead
    fields = ["ad", "first_name", "last_name", "email", "phone"]
    template_name = "leads/leads-create.html"
    success_url = reverse_lazy("leads:leads-list")


class LeadDeleteView(CustomDeleteView):
    model = Lead
    template_name = "leads/leads-delete.html"
    success_url = reverse_lazy("leads:leads-list")


class LeadDetailView(DetailView):
    template_name = "leads/leads-detail.html"
    queryset = Lead.objects.select_related("ad")


class LeadUpdateView(CustomUpdateView):
    model = Lead
    fields = ["ad", "first_name", "last_name", "email", "phone"]
    template_name = "leads/leads-edit.html"
