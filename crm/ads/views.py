from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F, Prefetch, QuerySet, Sum
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
)

from crm.views_custom import (
    CustomCreateView,
    CustomDeleteView,
    CustomUpdateView,
    PermissionsMixin,
)
from products.models import Product

from .models import Ad


class AdsList(PermissionsMixin, ListView):
    """
    Список рекламных компаний
    """

    template_name: str = "ads/ads-list.html"
    queryset: QuerySet[Ad] = Ad.objects.only("name")
    context_object_name: str = "ads"
    permission_required: str = "ads.view_ad"


class AdCreateView(PermissionsMixin, CustomCreateView):
    """
    Создание новой рекламной компании
    """

    model: type[Ad] = Ad
    fields: list[str] = ["product", "name", "promotionChannel", "budget"]
    template_name: str = "ads/ads-create.html"
    success_url: str = reverse_lazy("ads:ads-list")
    permission_required: str = "ads.add_ad"


class AdDeleteView(PermissionsMixin, CustomDeleteView):
    """
    Удаление рекламной компании
    """

    model: type[Ad] = Ad
    template_name: str = "ads/ads-delete.html"
    success_url: str = reverse_lazy("ads:ads-list")
    permission_required: str = "ads.delete_ad"


class AdDetailView(PermissionsMixin, DetailView):
    """
    Детализация рекламной компании
    """

    template_name: str = "ads/ads-detail.html"
    product_qs: QuerySet[Product] = Product.objects.only("name")
    queryset: QuerySet[Ad] = Ad.objects.prefetch_related(
        (Prefetch("product", queryset=product_qs))
    ).defer("promotionChannel", "created_by_id")
    permission_required: str = "ads.view_ad"


class AdUpdateView(PermissionsMixin, CustomUpdateView):
    """
    Обновление данных о рекламной компании
    """

    model: type[Ad] = Ad
    fields: list[str] = ["product", "name", "promotionChannel", "budget"]
    template_name: str = "ads/ads-edit.html"
    permission_required: str = "ads.change_ad"


class AdStatisticView(LoginRequiredMixin, TemplateView):
    """
    Общая статистика CRM
    """

    template_name = "ads/ads-statistic.html"

    def get(self, request, *args, **kwargs) -> TemplateResponse:
        context: dict[str, Any] = self.get_context_data(**kwargs)
        ads: QuerySet[Ad] = (
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
