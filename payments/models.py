from django.db import models
from django.conf import settings

from invoices.models import Invoice


# Create your models here.
class Payment(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return str(self.id)
