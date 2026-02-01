"""
Модуль для моделей приложения products.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import (
    PROTECT,
    CharField,
    DateTimeField,
    DecimalField,
    FileField,
    ForeignKey,
)


from products.models import Product

User = get_user_model()

def user_contract_dir_path(filename: str) -> str:
    """
    Получение пути для сохранения переданного файла
    :param filename:
    :return:
    """
    path = f"contracts/{filename}"
    return path


class Contract(models.Model):
    """
    Модель для контрактов
    """
    created_by = ForeignKey(User, on_delete=PROTECT, editable=False)
    product = ForeignKey(Product, on_delete=PROTECT, related_name="contracts")
    file = FileField(upload_to=user_contract_dir_path)
    name = CharField(max_length=100, db_index=True)
    start_date = DateTimeField()
    end_date = DateTimeField()
    cost = DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"
