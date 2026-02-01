"""
Модуль представлений приложения customers
"""

# pylint: disable=too-many-ancestors

from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
)

from ads.models import Ad
from crm.views_custom import (
    CustomCreateView,
    CustomDeleteView,
    CustomUpdateView,
    PermissionsMixin,
)

from .models import Lead

class LeadsListView(PermissionsMixin, ListView):
    """
    Список потенциальных клиентов
    """
    template_name = "leads/leads-list.html"
    context_object_name = "leads"
    queryset = Lead.objects.only("first_name", "last_name")
    permission_required = "leads.view_lead"


class LeadCreateView(PermissionsMixin, CustomCreateView):
    """
    Создание потенциального клиента
    """
    model = Lead
    fields = ["ad", "first_name", "last_name", "email", "phone"]
    template_name = "leads/leads-create.html"
    success_url = reverse_lazy("leads:leads-list")
    permission_required = "leads.add_lead"


class LeadDeleteView(PermissionsMixin, CustomDeleteView):
    """
    Удаление потенциального клиента
    """
    model = Lead
    template_name = "leads/leads-delete.html"
    success_url = reverse_lazy("leads:leads-list")
    permission_required = "leads.delete_lead"


class LeadDetailView(PermissionsMixin, DetailView):
    """
    Детализация потенциального клиента
    """
    template_name = "leads/leads-detail.html"
    ad_qs = Ad.objects.only("name")
    queryset = Lead.objects.prefetch_related((Prefetch("ad", queryset=ad_qs))).defer(
        "created_by"
    )
    permission_required = "leads.view_lead"


class LeadUpdateView(PermissionsMixin, CustomUpdateView):
    """
    Редактирование потенциального клиента
    """
    model = Lead
    fields = ["ad", "first_name", "last_name", "email", "phone"]
    template_name = "leads/leads-edit.html"
    permission_required = "leads.change_lead"
