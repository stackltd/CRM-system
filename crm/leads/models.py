"""
Модуль моделей приложения leads.
"""


from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import (
    PROTECT,
    CharField,
    EmailField,
    ForeignKey,
)
from phonenumber_field.modelfields import PhoneNumberField

from ads.models import Ad

User = get_user_model()

class Lead(models.Model):
    """
    Модель потенциальных клиентов приложения leads
    """
    created_by = ForeignKey(User, on_delete=PROTECT, editable=False)
    ad = ForeignKey(Ad, on_delete=PROTECT, related_name="leads")
    first_name = CharField(max_length=100, db_index=True)
    last_name = CharField(max_length=100, db_index=True)
    email = EmailField(null=False, blank=True, db_index=True)
    phone = PhoneNumberField(unique=True, region=None, db_index=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
