from django.test import TestCase
from leaves.models import Leave
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from leaves.views import LeaveList, LeaveUpdate
from datetime import datetime, timedelta

# Create your tests here.
class LeaveModelTest(TestCase):
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

    def test_create_leave(self):
        user = get_user_model().objects.get(email='test@email.com')
        leave = Leave.objects.create(user=user,
                            commencement_date=datetime.today(),
                            duration=10,
                            body='Test Leave'
                        )
        
        self.assertEqual(leave.is_approved, False)
        self.assertEqual(leave.applied_date, datetime.today().date())
    
    def test_register_leave(self):
        user = get_user_model().objects.get(email='test@email.com')
        factory = APIRequestFactory()
        request = factory.post('', 
                        {
                            'body':'Test leave', 
                            'commencement_date':datetime.today().strftime("%Y-%m-%d"), 
                            'end_date':(datetime.today()+timedelta(days=10)).strftime("%Y-%m-%d")
                        }, 
                        format='json')
        view = LeaveList.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 201)
    
    def test_fetch_leaves(self):
        user = get_user_model().objects.get(email='test@email.com')
        factory = APIRequestFactory()
        request = factory.get('')
        view = LeaveList.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
    
    def test_approve_leave(self):
        user = get_user_model().objects.get(email='test@email.com')
        user.typeAccount = 'CATERER'
        user.save()
        leave = Leave.objects.create(user=user,
                            commencement_date=datetime.today(),
                            duration=10,
                            body='Test Leave'
                        )
        self.assertEqual(leave.is_approved, False)

        factory = APIRequestFactory()
        request = factory.patch('approve/%s/'%leave.id, {'is_approved':True}, format='json')
        view = LeaveUpdate.as_view()
        force_authenticate(request, user=user)
        response = view(request, pk=leave.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Leave.objects.get(id=leave.id).is_approved, True)

