from django.contrib.auth.models import User
from django.db import models
from django.db.models import (
    CharField,
    TextField,
    DecimalField,
    SmallIntegerField,
    DateTimeField,
    BooleanField,
    FileField,
    ForeignKey,
    PROTECT,
)

from products.models import Product


def user_contract_dir_path(inst: "Contract", filename: str) -> str:
    path = f"contracts/{filename}"
    return path


class Contract(models.Model):
    created_by = ForeignKey(User, on_delete=PROTECT, editable=False)
    product = ForeignKey(Product, on_delete=PROTECT, related_name="contracts")
    file = FileField(upload_to=user_contract_dir_path)
    name = CharField(max_length=100)
    start_date = DateTimeField()
    end_date = DateTimeField()
    cost = DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"
