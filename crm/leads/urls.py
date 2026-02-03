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
