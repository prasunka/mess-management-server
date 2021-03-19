from django.urls import path
from .views import CouponList, buyCoupon, verifyPayment

urlpatterns = [
    path("", CouponList.as_view()),
    path("buy/request/", buyCoupon),
    path("buy/confirm/", verifyPayment),
]
