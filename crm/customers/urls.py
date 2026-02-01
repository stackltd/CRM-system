"""
URL‑конфигурация приложения customers.

Содержит маршруты:
- /customers/ — список клиентов;
- /customers/new/ — создание клиента;
- /customers/<int:pk>/ — детализация клиента;
- /customers/<int:pk>/edit/ — редактирование клиентов;
- /customers/<int:pk>/delete/ — удаление клиентов;
"""


from django.urls import path

from .views import (
    CustomerCreateView,
    CustomerDeleteView,
    CustomerDetailView,
    CustomersListView,
    CustomerUpdateView,
)

app_name = "customers"

urlpatterns = [
    path("", CustomersListView.as_view(), name="customers-list"),
    path("new/", CustomerCreateView.as_view(), name="customer-create"),
    path("<int:pk>/delete/", CustomerDeleteView.as_view(), name="customer-delete"),
    path("<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("<int:pk>/edit/", CustomerUpdateView.as_view(), name="customer-update"),
]
