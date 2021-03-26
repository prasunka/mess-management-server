from django.urls import path
from .views import BillsList, payBill, verifyPayment

urlpatterns = [
    path("", BillsList.as_view()),
    path("pay/request/", payBill),
    path("pay/confirm/", verifyPayment),
]