from django.urls import path
from .views import BillsList, payBill, verifyPayment
from .views import downloadReport, generateBill

urlpatterns = [
    path("", BillsList.as_view()),
    path("pay/request/", payBill),
    path("pay/confirm/", verifyPayment),
    path("report/", downloadReport),
    path("generate/", generateBill)
]