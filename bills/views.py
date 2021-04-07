import environ
import io
import csv
import json
import razorpay

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.core.management import call_command

from rest_framework import generics, status
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
        if self.request.user.typeAccount == 'CATERER':
           return Bill.objects.all()
            
        return Bill.objects.filter(buyer=self.request.user.id)


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

@api_view(['GET'])
def downloadReport(request):

    if request.user.typeAccount != 'CATERER':
           return Response(status=status.HTTP_404_NOT_FOUND)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Email', 'Name', 'Due Bill'])
    for user in get_user_model().objects.all():
        bills = Bill.objects.filter(buyer=user.id)\
            .filter(is_paid=False)\
            .aggregate(Sum('bill_amount'))
        
        if bills['bill_amount__sum'] is None:
            continue

        #print(bills['bill_amount__sum'])
        writer.writerow([user.email, user.name, bills['bill_amount__sum']])
    
    return response

@api_view(['POST'])
def generateBill(request):
    if request.user.typeAccount != 'CATERER':
           return Response(status=status.HTTP_404_NOT_FOUND)

    with io.StringIO() as out:
        call_command('generatebill', stdout=out)
        res = out.getvalue()
        if 'has already been generated.' in res:
            return Response( {'success':0, 'message': res}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            lines = res.split('\n')
            months = []
            for line in lines:
                if line.startswith('Generating bill for '):
                    months.append(int(line.split("Generating bill for ")[1]))
            return Response({'success':1, 'months':months})
