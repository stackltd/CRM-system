"""
Модуль моделей приложения customers.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import PROTECT, ForeignKey

from contracts.models import Contract
from leads.models import Lead

User = get_user_model()


class Customer(models.Model):
    """
    Модель клиента приложения customers
    """
    created_by = ForeignKey(User, on_delete=PROTECT, editable=False)
    lead = ForeignKey(Lead, on_delete=PROTECT, related_name="customers")
    contract = ForeignKey(Contract, on_delete=PROTECT, related_name="customers")

    def __str__(self):
        return f"{self.lead.first_name} {self.lead.last_name}: {self.contract.name}"
