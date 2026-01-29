from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    next_page = "/"


class CustomLogoutView(LogoutView):
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("registration:login")
