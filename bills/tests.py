from django.test import TestCase
from bills.models import Bill, BillGenerationHistory
from invoices.models import Invoice
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from bills.views import BillsList, downloadReport, generateBill, payBill
from datetime import datetime

# Create your tests here.
class BillModelTest(TestCase):
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
    
    def test_fetch_bills(self):
        user = get_user_model().objects.get(email='test@email.com')
        factory = APIRequestFactory()
        request = factory.get('')
        view = BillsList.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
    
    def test_pay_bills(self):
        user = get_user_model().objects.get(email='test@email.com')
        bill = Bill.objects.create(buyer=user, bill_from=datetime.today().replace(day=1),
                            bill_amount=4000, bill_days=30)

        factory = APIRequestFactory()
        request = factory.post('pay/request/', {'id':bill.id}, format='json')
        view = payBill
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['order_id']!=None)
    
    def test_download_report(self):
        user = get_user_model().objects.get(email='test@email.com')
        user.typeAccount = 'CATERER'
        user.save()

        factory = APIRequestFactory()
        request = factory.get('report/')
        view = downloadReport
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
    
    def test_generate_bill(self):
        user = get_user_model().objects.get(email='test@email.com')
        user.typeAccount = 'CATERER'
        user.save()

        factory = APIRequestFactory()
        request = factory.post('generate/', {}, format='json')
        view = generateBill
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
    
    def test_create_bill_generation_history(self):
        user = get_user_model().objects.get(email='test@email.com')

        history = BillGenerationHistory.objects.create(
            date=datetime.today(), numBills=10, totalAmount=40000
        )
        
        self.assertEqual(history.__str__(), str(history.id) + ' - ' + str(history.date.month) + '/' + str(history.date.year))
    
        
