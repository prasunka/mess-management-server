from django.contrib import admin

from .models import Leave
# Register your models here.

class LeaveAdmin(admin.ModelAdmin):
    readonly_fields = ('applied_date', 'approved_date', 'get_end_date')
    
    class Meta:
        model = Leave

admin.site.register(Leave, LeaveAdmin)