from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import (
    CharField,
    TextField,
    DecimalField,
    ForeignKey,
    PROTECT,
)


class Product(models.Model):
    created_by = ForeignKey(User, on_delete=PROTECT, editable=False)
    name = CharField(max_length=100)
    description = TextField()
    cost = DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.name}"
