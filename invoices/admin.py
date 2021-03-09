from django.contrib import admin
from .models import Invoice

# Register your models here.
class InvoiceAdmin(admin.ModelAdmin):
    class Meta:
        model = Invoice

admin.site.register(Invoice, InvoiceAdmin)