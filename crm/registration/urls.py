"""
URL‑конфигурация приложения products.

Содержит маршруты:
- /accounts/login — авторизация в системе;
- /accounts/logout/ — выход из системы;
"""

from django.urls import path

from .views import CustomLoginView, CustomLogoutView

app_name = "registration"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
