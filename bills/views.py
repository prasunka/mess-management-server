import environ
import json
import razorpay
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from invoices.models import Invoice
from payments.models import Payment
from .models import Bill
from .serializers import BillSerializer
# Create your views here.

class BillsList(generics.ListAPIView):
    serializer_class = BillSerializer

    def get_queryset(self):
        return Bill.objects.filter(buyer=self.request.user)


orders = {}


@api_view(['POST'])
def payBill(request):
    if request.method == 'POST':
        env = environ.Env(
            DEBUG=(bool, False)
        )
        environ.Env.read_env()
        RAZORPAY_ID = env('RAZORPAY_ID')
        RAZORPAY_SECRET_KEY = env('RAZORPAY_SECRET_KEY')

        client = razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_SECRET_KEY))
        try:
            request_body = json.loads(request.body.decode('utf-8'))
            bill_id = request_body['id']
        except (KeyError, json.JSONDecodeError):
            return Response({'message': 'Please supply bill id'})

        try:
            bill = Bill.objects.get(id=bill_id)
        except:
            return Response({'message': 'Invalid ID'})

        DATA = {}
        DATA['currency'] = 'INR'
        DATA['amount'] = int(bill.bill_amount * 100)
        DATA['notes'] = {'type': 'bill', 'paid_by': request.user.email, 'bill_id': bill.id,
                         'bill_month': bill.get_month(), 'bill_year': bill.get_year()}

        order = client.order.create(data=DATA)
        # print(order)
        orders[request.user.email] = order

        return Response({'order_id': order['id']})


@api_view(['POST'])
def verifyPayment(request):
    request_body = json.loads(request.body.decode('utf-8'))
    print(request_body)

    params = {}
    try:
        params['razorpay_payment_id'] = request_body['payment_id']
        params['razorpay_signature'] = request_body['signature']
    except KeyError:
        return Response({'message': 'Provide both payment_id and signature'})

    try:
        params['razorpay_order_id'] = orders[request.user.email]['id']
    except KeyError:
        return Response({'message': 'No order found for this user'})

    env = environ.Env(
        DEBUG=(bool, False)
    )
    environ.Env.read_env()
    RAZORPAY_ID = env('RAZORPAY_ID')
    RAZORPAY_SECRET_KEY = env('RAZORPAY_SECRET_KEY')
    client = razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_SECRET_KEY))

    result = 1
    try:
        client.utility.verify_payment_signature(params)
    except razorpay.errors.SignatureVerificationError:
        result = 0

    if result == 1:
        order = client.order.fetch(params['razorpay_order_id'])
        invoice = Invoice(type='bill', order_id=order['id'])
        invoice.save()

        payment = Payment(buyer=request.user, invoice=invoice, amount=order['amount'] / 100)
        payment.save()

        bill = Bill.objects.get(id=order['notes']['bill_id'])
        bill.is_paid = True
        bill.save()
        

    return Response({'success': result})
