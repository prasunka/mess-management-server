from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from users.models import ModeHistory
from users.views import ModeUpdate
from datetime import datetime
# Create your tests here.

class UserModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@email.com',
            name='test123',
            typeAccount='test',
            specialRole='test_role',
            password='password123'
        )
        
        self.assertEqual(user.email, 'test@email.com')
        self.assertEqual(user.name, 'test123')
        self.assertEqual(user.typeAccount, 'test')
        self.assertEqual(user.specialRole, 'test_role')
        self.assertEqual(user.billingMode, 'MONTHLY')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            email='test2@email.com',
            name='test123',
            typeAccount='test',
            specialRole='test_role',
            password='password123'
        )
        
        self.assertEqual(user.email, 'test2@email.com')
        self.assertEqual(user.name, 'test123')
        self.assertEqual(user.typeAccount, 'test')
        self.assertEqual(user.specialRole, 'test_role')
        self.assertEqual(user.billingMode, 'MONTHLY')
        self.assertTrue(user.check_password('password123'))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
    
    def test_create_mode_history(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@email.com',
            name='test123',
            typeAccount='test',
            specialRole='test_role',
            password='password123'
        )

        history = ModeHistory.objects.create(
            user=user,
            dateChanged=datetime.today().date(),
            mode='COUPON'
        )
        
        self.assertEqual(history.dateChanged, datetime.today().date())
    
    def test_mode_change(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@email.com',
            name='test123',
            typeAccount='test',
            specialRole='test_role',
            password='password123'
        )
        
        self.assertEqual(user.requestedBillingMode, None)

        factory = APIRequestFactory()
        request = factory.patch(reverse('update_mode', kwargs={'pk':user.id}), {'requestedBillingMode':'COUPON'}, format='json')
        view = ModeUpdate.as_view()
        force_authenticate(request, user=user)
        response = view(request, pk=user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=user.id).requestedBillingMode, 'COUPON')



