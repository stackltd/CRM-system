from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, PROTECT


from leads.models import Lead
from contracts.models import Contract


class Customer(models.Model):
    created_by = ForeignKey(User, on_delete=PROTECT, editable=False)
    lead = ForeignKey(Lead, on_delete=PROTECT, related_name="customers")
    contract = ForeignKey(Contract, on_delete=PROTECT, related_name="customers")

    def __str__(self):
        return f"{self.lead.first_name} {self.lead.last_name}: {self.contract.name}"
