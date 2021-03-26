from django.contrib import admin
from .models import Bill
# Register your models here.


class BillAdmin(admin.ModelAdmin):
    fields = ('buyer', 'is_paid', 'bill_from', 'bill_days', 'bill_amount','invoice')
    class Meta:
        model = Bill

admin.site.register(Bill, BillAdmin)