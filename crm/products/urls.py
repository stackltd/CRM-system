"""
URL‑конфигурация приложения products.

Содержит маршруты:
- /products/ — список услуг;
- /products/new/ — создание услуги;
- /products/<int:pk>/ — детализация услуги;
- /products/<int:pk>/edit/ — редактирование услуги;
- /products/<int:pk>/delete/ — удаление услуги;
"""

from django.urls import path

from .views import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductsList,
    ProductUpdateView,
)

app_name = "products"

urlpatterns = [
    path("", ProductsList.as_view(), name="products-list"),
    path("new/", ProductCreateView.as_view(), name="product-create"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("<int:pk>/edit/", ProductUpdateView.as_view(), name="product-update"),
]
