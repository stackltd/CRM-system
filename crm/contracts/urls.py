from django.urls import path

from .views import (
    ContractCreateView,
    ContractDeleteView,
    ContractDetailView,
    ContractsListView,
    ContractUpdateView,
)

app_name = "contracts"

urlpatterns = [
    path("", ContractsListView.as_view(), name="contracts-list"),
    path("new/", ContractCreateView.as_view(), name="contract-create"),
    path("<int:pk>/delete/", ContractDeleteView.as_view(), name="contract-delete"),
    path("<int:pk>/", ContractDetailView.as_view(), name="contract-detail"),
    path("<int:pk>/edit/", ContractUpdateView.as_view(), name="contract-update"),
]
