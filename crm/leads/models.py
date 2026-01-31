from django.contrib.auth.models import User
from django.db import models
from django.db.models import (
    CharField,
    ForeignKey,
    PROTECT,
    EmailField,
)

from phonenumber_field.modelfields import PhoneNumberField

from ads.models import Ad


class Lead(models.Model):
    created_by = ForeignKey(User, on_delete=PROTECT, editable=False)
    ad = ForeignKey(Ad, on_delete=PROTECT, related_name="leads")
    first_name = CharField(max_length=100, db_index=True)
    last_name = CharField(max_length=100, db_index=True)
    email = EmailField(null=False, blank=True, db_index=True)
    phone = PhoneNumberField(unique=True, region=None, db_index=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
