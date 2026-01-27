
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Ad

class AdsList(ListView):    
    template_name = "ads/ads-list.html"
    queryset = Ad.objects.select_related("product")
    context_object_name = "ads"


class AdCreateView(CreateView):
    model = Ad
    fields = ["product", "name", "promotionChannel", "budget"]
    template_name = "ads/ads-create.html"
    success_url = reverse_lazy("ads:ads-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save(commit=False)
        resp = super().form_valid(form)
        return resp


class AdDeleteView(DeleteView):
    model = Ad
    template_name = "ads/ads-delete.html"
    success_url = reverse_lazy("ads:ads-list")


class AdDetailView(DetailView):    
    template_name = "ads/ads-detail.html"
    queryset = Ad.objects.select_related("product")


class AdUpdateView(UpdateView):
    model = Ad
    fields = ["product", "name", "promotionChannel", "budget"]
    template_name = "ads/ads-edit.html"

    def get_success_url(self):
        url = reverse("ads:ad-detail", kwargs={"pk": self.object.pk})
        return url



class AdStatisticView(TemplateView):
    template_name = "ads/ads-statistic.html"
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["ads"] = Ad.objects.all()
        return self.render_to_response(context)