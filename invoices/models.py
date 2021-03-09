from django.db import models

# Create your models here.
class Invoice(models.Model):
    TYPE_CHOICES = [
        ('bill', 'bill'),
        ('coupon', 'coupon'),
    ]
    type = models.CharField(choices=TYPE_CHOICES, blank=False, null=False, max_length=10)
    order_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id) + " - " + str(self.type)