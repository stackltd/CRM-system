from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import (
    CharField,
    DecimalField,
    ForeignKey,
    PROTECT,
)

from products.models import Product


class Ad(models.Model):
    created_by = ForeignKey(User, on_delete=PROTECT, editable=False)
    product = ForeignKey(Product, on_delete=PROTECT, related_name="ads")
    name = CharField(max_length=100)
    promotionChannel = CharField(max_length=100, null=False, blank=True)
    budget = DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}"

