from django.urls import path
from .views import BillsList, payBill, verifyPayment
from .views import downloadReport

urlpatterns = [
    path("", BillsList.as_view()),
    path("pay/request/", payBill),
    path("pay/confirm/", verifyPayment),
    path("report/", downloadReport),
]