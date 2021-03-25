from django.contrib import admin

from .models import Complaint

# Register your models here.
class ComplaintAdmin(admin.ModelAdmin):
    class Meta:
        model = Complaint

admin.site.register(Complaint, ComplaintAdmin)