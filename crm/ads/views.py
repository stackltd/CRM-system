from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F, Sum, Prefetch
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)

from .models import Ad
from leads.models import Lead
from products.models import Product
from crm.views_custom import CustomDeleteView, CustomCreateView, CustomUpdateView, PermissionsMixin


class AdsList(PermissionsMixin, ListView):
    template_name = "ads/ads-list.html"
    queryset = Ad.objects.only("name")
    context_object_name = "ads"
    permission_required = "ads.view_ad"


class AdCreateView(PermissionsMixin, CustomCreateView):
    model = Ad
    fields = ["product", "name", "promotionChannel", "budget"]
    template_name = "ads/ads-create.html"
    success_url = reverse_lazy("ads:ads-list")
    permission_required = "ads.add_ad"


class AdDeleteView(PermissionsMixin, CustomDeleteView):
    model = Ad
    template_name = "ads/ads-delete.html"
    success_url = reverse_lazy("ads:ads-list")
    permission_required = "ads.delete_ad"


class AdDetailView(PermissionsMixin, DetailView):
    template_name = "ads/ads-detail.html"
    product_qs = Product.objects.only("name")
    queryset = Ad.objects.prefetch_related((Prefetch("product", queryset=product_qs))).defer("promotionChannel", "created_by_id")
    permission_required = "ads.view_ad"


class AdUpdateView(PermissionsMixin, CustomUpdateView):
    model = Ad
    fields = ["product", "name", "promotionChannel", "budget"]
    template_name = "ads/ads-edit.html"
    permission_required = "ads.change_ad"


class AdStatisticView(LoginRequiredMixin , TemplateView):
    template_name = "ads/ads-statistic.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        ads = (
            Ad.objects
            # .select_related("product").prefetch_related("leads__customers")
            .annotate(
                leads_count=Count("leads", distinct=True),
                customers_count=Count("leads__customers", distinct=True),
                contracts_income=Sum(
                    "product__contracts__cost",
                    distinct=True,
                ),
                profit=F("contracts_income") - F("budget"),
            ).order_by("-leads_count", "-customers_count")
        )
        context["ads"] = ads
        return self.render_to_response(context)

