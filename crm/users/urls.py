"""
URL‑конфигурация приложения products.

Содержит маршруты:
- "/" — Статистика CRM;
"""


from django.urls import path

from .views import GenStatView

app_name = "users"

urlpatterns = [
    path("", GenStatView.as_view(), name="statistic"),
]
