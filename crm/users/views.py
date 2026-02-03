from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
)

from ads.models import Ad
from contracts.models import Contract
from customers.models import Customer
from leads.models import Lead
from products.models import Product


class GenStatView(LoginRequiredMixin, TemplateView):
    """
    Сбор статистики CRM системы
    """

    template_name = "users/index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        for model in (Product, Ad, Lead, Customer, Contract):
            context.update(
                {f"{model._meta.verbose_name_plural}_count": model.objects.count()}
            )
        return self.render_to_response(context)
