"""
URL‑конфигурация приложения leads.

Содержит маршруты:
- /leads/ — список потенциальных клиентов;
- /leads/new/ — создание потенциального клиента;
- /leads/<int:pk>/ — детализация потенциального клиента;
- /leads/<int:pk>/edit/ — редактирование потенциального клиента;
- /leads/<int:pk>/delete/ — удаление потенциального клиента;
"""

from django.urls import path

from .views import (
    LeadCreateView,
    LeadDeleteView,
    LeadDetailView,
    LeadsListView,
    LeadUpdateView,
)

app_name = "leads"

urlpatterns = [
    path("", LeadsListView.as_view(), name="leads-list"),
    path("new/", LeadCreateView.as_view(), name="lead-create"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="lead-create"),
    path("<int:pk>/", LeadDetailView.as_view(), name="lead-detail"),
    path("<int:pk>/edit/", LeadUpdateView.as_view(), name="lead-update"),
]
