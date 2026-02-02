"""
Модуль представлений приложения registration
"""

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    """
    Вход в систему
    """

    redirect_authenticated_user = True
    next_page = "/"


class CustomLogoutView(LogoutView):
    """
    Выход из системы
    """

    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("registration:login")
