from django.test import TestCase
from django.contrib.auth import get_user_model

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
        self.assertTrue(user.check_password('password123'))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)