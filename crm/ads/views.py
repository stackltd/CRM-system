from django.db.models import Count, F, Sum
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)

from .models import Ad
from leads.models import Lead
from crm.views_custom import CustomDeleteView, CustomCreateView, CustomUpdateView


class AdsList(ListView):
    template_name = "ads/ads-list.html"
    queryset = Ad.objects.select_related("product")
    context_object_name = "ads"


class AdCreateView(CustomCreateView):
    model = Ad
    fields = ["product", "name", "promotionChannel", "budget"]
    template_name = "ads/ads-create.html"
    success_url = reverse_lazy("ads:ads-list")


class AdDeleteView(CustomDeleteView):
    model = Ad
    template_name = "ads/ads-delete.html"
    success_url = reverse_lazy("ads:ads-list")


class AdDetailView(DetailView):
    template_name = "ads/ads-detail.html"
    queryset = Ad.objects.select_related("product")


class AdUpdateView(CustomUpdateView):
    model = Ad
    fields = ["product", "name", "promotionChannel", "budget"]
    template_name = "ads/ads-edit.html"


class AdStatisticView(TemplateView):
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
