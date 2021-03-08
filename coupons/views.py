from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
import razorpay
import os, environ

from .models import Coupon
from .serializers import CouponSerializer

# Create your views here.
class CouponList(generics.ListAPIView):
    serializer_class = CouponSerializer

    def get_queryset(self):
        return Coupon.objects.filter(buyer=self.request.user)

orders = {}

@api_view(['POST'])
def buyCoupon(request):
    if request.method == 'POST':
        env = environ.Env(
            DEBUG=(bool, False)
        )
        environ.Env.read_env()
        RAZORPAY_ID = env('RAZORPAY_ID')
        RAZORPAY_SECRET_KEY = env('RAZORPAY_SECRET_KEY')

        client = razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_SECRET_KEY))
        DATA = {}
        DATA['currency'] = 'INR'
        DATA['amount'] = 12600
        DATA['notes'] = {'type':'coupon', 'buyer':request.user.email}

        order = client.order.create(data=DATA)
        #print(order)
        orders[request.user.email] = order

        return Response({'order_id': order['id']})

@api_view(['POST'])
def verifyPayment(request):
    print(request.POST)

    params = {}
    try:
        params['razorpay_payment_id'] = request.POST['payment_id']
        params['razorpay_signature'] = request.POST['signature']
    except KeyError:
        return Response({'message':'Provide both payment_id and signature'})
    
    try:
        params['razorpay_order_id'] = 'order_GjqjlMhZWry5QR'# orders[request.user.email]
    except KeyError:
        return Response({'message':'No order found for this user'})
    
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


    return Response({'success' : result})


