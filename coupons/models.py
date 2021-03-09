import uuid
from django.db import models
from django.conf import settings

from invoices.models import Invoice

# Create your models here.
class Coupon(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_spent = models.BooleanField(default=False)
    spent_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)

