"""
Модуль для кастомизации форм приложения contracts.
"""

from django import forms
from django.forms import FileField

from .models import Contract


class ContractForm(forms.ModelForm):
    """
    Кастомизация форм приложения contracts для создания возможности выборы даты в UpdateView
    """

    class Meta:
        model = Contract
        fields = ["product", "name", "start_date", "end_date", "cost", "file"]
        widgets = {
            "start_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
            "end_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
        }

    file = FileField()
