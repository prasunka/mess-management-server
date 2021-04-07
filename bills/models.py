from django.db import models
from django.conf import settings
from django.utils import timezone
from payments.models import Payment
from invoices.models import Invoice

# Create your models here.
class Bill(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    bill_from = models.DateField()
    bill_days = models.IntegerField()
    bill_amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return str(self.buyer)

    def get_month(self):
        return self.bill_from.month

    def get_year(self):
        return self.bill_from.year

class BillGenerationHistory(models.Model):
    date = models.DateField(default=timezone.now)
    numBills = models.IntegerField()
    totalAmount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.date.month) + '/' + str(self.date.year)

    class Meta:
        verbose_name_plural = "Bill generation histories"