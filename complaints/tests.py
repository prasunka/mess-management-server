from django.test import TestCase
from complaints.models import Complaint
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from complaints.views import ComplaintList, ComplaintUpdate
from datetime import datetime

# Create your tests here.
class ComplaintModelTest(TestCase):
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

    def test_create_complaint(self):
        user = get_user_model().objects.get(email='test@email.com')
        complaint = Complaint.objects.create(user=user,
                            title="Test title",
                            body="Test body",
                        )
        
        self.assertEqual(complaint.resolved, False)
        self.assertEqual(complaint.applied_date, datetime.today().date())
    
    def test_register_complaint(self):
        user = get_user_model().objects.get(email='test@email.com')
        factory = APIRequestFactory()
        request = factory.post('', {'title':'Test title 2', 'body':'Test body 2'}, format='json')
        view = ComplaintList.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 201)
    
    def test_fetch_complaint(self):
        user = get_user_model().objects.get(email='test@email.com')
        factory = APIRequestFactory()
        request = factory.get('')
        view = ComplaintList.as_view()
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
    
    def test_resolve_complaint(self):
        user = get_user_model().objects.get(email='test@email.com')
        user.typeAccount = 'CATERER'
        user.save()
        complaint = Complaint.objects.create(user=user, title='Test title',
                                            body='Test body')
        self.assertEqual(complaint.resolved, False)

        factory = APIRequestFactory()
        request = factory.patch('resolve/%s/'%complaint.id, {'resolved':True}, format='json')
        view = ComplaintUpdate.as_view()
        force_authenticate(request, user=user)
        response = view(request, pk=complaint.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Complaint.objects.get(id=complaint.id).resolved, True)

