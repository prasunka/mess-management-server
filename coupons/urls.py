from django.urls import path
from .views import CouponList, buyCoupon, verifyPayment
from .views import spendCoupon

urlpatterns = [
    path("", CouponList.as_view()),
    path("buy/request/", buyCoupon),
    path("buy/confirm/", verifyPayment),
    path("spend/<uuid>/", spendCoupon),
]
