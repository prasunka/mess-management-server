from django.contrib import admin
from .models import Payment

# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    class Meta:
        model = Payment

admin.site.register(Payment, PaymentAdmin)