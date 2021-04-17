from django.test import TestCase
from coupons.models import Coupon
from invoices.models import Invoice
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from coupons.views import CouponList, buyCoupon, spendCoupon
from datetime import datetime

# Create your tests here.
class CouponModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        User = get_user_model()
        User.objects.create_user(
            email='test@email.com',
            name='test123',
            typeAccount='test',
            specialRole='test_role',
            password='password123'
        )
    
    def test_fetch_coupons(self):
        user = get_user_model().objects.get(email='test@email.com')
        factory = APIRequestFactory()
        request = factory.get('')
        view = CouponList.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
    
    def test_buy_coupons(self):
        user = get_user_model().objects.get(email='test@email.com')
        factory = APIRequestFactory()
        request = factory.post('buy/request/', {}, format='json')
        view = buyCoupon
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['order_id']!=None)
    
    def test_spend_coupons(self):
        user = get_user_model().objects.get(email='test@email.com')
        user.typeAccount = 'CATERER'
        user.save()

        invoice = Invoice.objects.create(type='coupon', order_id='order_id#123')
        coupon = Coupon.objects.create(buyer=user, invoice=invoice)

        factory = APIRequestFactory()
        request = factory.get('spend/%s/'%coupon.uuid)
        view = spendCoupon
        force_authenticate(request, user=user)
        response = view(request, uuid=coupon.uuid)

        self.assertEqual(response.status_code, 200)
        
