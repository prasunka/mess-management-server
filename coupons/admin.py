from django.contrib import admin
from .models import Coupon


# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'timestamp', 'spent_timestamp')

    class Meta:
        model = Coupon


admin.site.register(Coupon, CouponAdmin)
