"""
Модуль представлений приложения customers
"""

# pylint: disable=too-many-ancestors

from django.db.models import Prefetch, QuerySet
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

    template_name: str = "leads/leads-list.html"
    context_object_name: str = "leads"
    queryset: QuerySet[Lead] = Lead.objects.only("first_name", "last_name")
    permission_required: str = "leads.view_lead"


class LeadCreateView(PermissionsMixin, CustomCreateView):
    """
    Создание потенциального клиента
    """

    model: type[Lead] = Lead
    fields: list[str] = ["ad", "first_name", "last_name", "email", "phone"]
    template_name: str = "leads/leads-create.html"
    success_url: str = reverse_lazy("leads:leads-list")
    permission_required: str = "leads.add_lead"


class LeadDeleteView(PermissionsMixin, CustomDeleteView):
    """
    Удаление потенциального клиента
    """

    model: type[Lead] = Lead
    template_name: str = "leads/leads-delete.html"
    success_url: str = reverse_lazy("leads:leads-list")
    permission_required: str = "leads.delete_lead"


class LeadDetailView(PermissionsMixin, DetailView):
    """
    Детализация потенциального клиента
    """

    template_name: str = "leads/leads-detail.html"
    ad_qs: QuerySet[Ad] = Ad.objects.only("name")
    queryset: QuerySet[Lead] = Lead.objects.prefetch_related(
        (Prefetch("ad", queryset=ad_qs))
    ).defer("created_by")
    permission_required: str = "leads.view_lead"


class LeadUpdateView(PermissionsMixin, CustomUpdateView):
    """
    Редактирование потенциального клиента
    """

    model: type[Lead] = Lead
    fields: list[str] = ["ad", "first_name", "last_name", "email", "phone"]
    template_name: str = "leads/leads-edit.html"
    permission_required: str = "leads.change_lead"
