from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import User, Crypto, Transaction
from decimal import Decimal

class UpdateDeleteGetCryptoViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123', email='testuser@example.com'
        )
        self.client.login(username='testuser', password='password123')
        self.crypto = Crypto.objects.create(symbol='BTC', name='Bitcoin', current_price=Decimal('50000.00'))

    def test_get_crypto_data(self):
        url = reverse('crypto-history')  # Adjust URL name as per your URL config
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('BTC', response.data)

    def test_delete_all_cryptos(self):
        url = reverse('crypto-delete')  # Adjust URL name as per your URL config
        data = {'confirm_delete': True}

        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Crypto.objects.count(), 0)  # Ensure all cryptos are deleted

    def test_delete_all_cryptos_without_confirmation(self):
        url = reverse('crypto-delete')  # Adjust URL name as per your URL config
        data = {'confirm_delete': False}

        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Crypto.objects.count(), 1)  # Ensure no cryptos are deleted


class CryptoHistoryViewTest(APITestCase):

    def test_post_invalid_interval(self):
        url = reverse('crypto-history')  # Adjust URL name as per your URL config
        data = {
            'symbol': 'BTC',
            'interval': 'invalid_interval'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid interval', response.data['error'])

    def test_post_valid_request(self):
        url = reverse('crypto-history')  # Adjust URL name as per your URL config
        data = {
            'symbol': 'BTC',
            'interval': 'd1'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('symbol', response.data)
        self.assertIn('interval', response.data)

    def test_get_no_data_found(self):
        url = reverse('crypto-history')  # Adjust URL name as per your URL config
        response = self.client.get(url, {'symbol': 'BTC', 'interval': 'd1'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('No historical data found', response.data['error'])

