from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
)

from products.models import Product
from ads.models import Ad
from leads.models import Lead
from customers.models import Customer
from contracts.models import Contract


class GenStatView(LoginRequiredMixin, TemplateView):
    template_name = "users/index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        [
            context.update(
                {f"{model._meta.verbose_name_plural}_count": model.objects.count()}
            )
            for model in (Product, Ad, Lead, Customer, Contract)
        ]
        return self.render_to_response(context)
