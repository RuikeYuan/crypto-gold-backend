
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import User, Crypto, Transaction
from decimal import Decimal


class UserRegistrationViewTest(APITestCase):

    def test_user_registration_success(self):
        url = reverse('user-registration')  # Adjust URL name as per your URL config
        data = {
            "username": "testuser",
            "password": "password123",
            "email": "testuser@example.com"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)

    def test_user_registration_invalid_data(self):
        url = reverse('user-registration')  # Adjust URL name as per your URL config
        data = {
            "username": "testuser",  # Missing email and password
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)


class UserViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123', email='testuser@example.com'
        )
        self.client.login(username='testuser', password='password123')

    def test_portfolio(self):
        url = reverse('user-portfolio', kwargs={'pk': self.user.pk})

        # Assuming the user has some transactions (e.g., a buy transaction)
        transaction = Transaction.objects.create(
            user=self.user,
            asset=Crypto.objects.create(symbol="BTC", name="Bitcoin"),
            action='buy',
            quantity=Decimal('1.0'),
            price=Decimal('50000.00')
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('BTC', response.data)  # Check if the crypto symbol appears
        self.assertEqual(response.data['BTC']['quantity'], '1.0')
        self.assertEqual(response.data['BTC']['total_cost'], '50000.00')