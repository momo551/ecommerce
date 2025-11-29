from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile

class AccountsViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_register_page(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_page(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_registration(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_user_login(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(self.client.session['_auth_user_id'])
    
    def test_user_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertFalse(self.client.session.get('_auth_user_id'))

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            address='123 Test Street',
            postal_code='12345',
            city='Test City'
        )
    
    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.address, '123 Test Street')
        self.assertEqual(self.profile.postal_code, '12345')
        self.assertEqual(self.profile.city, 'Test City')
        self.assertEqual(str(self.profile), 'Profile of testuser')
