from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Crypto, Metal, Transaction, Post, Reply, PriceHistory, Asset

class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CryptoTests(APITestCase):
    def test_create_crypto(self):
        url = reverse('crypto-list')
        data = {'rank': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'current_price': '50000.00'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class MetalTests(APITestCase):
    def test_create_metal(self):
        url = reverse('metal-list')
        data = {'name': 'Gold', 'symbol': 'AU', 'current_price': '1800.00'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TransactionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.asset = Asset.objects.create(name='Bitcoin', symbol='BTC')

    def test_create_transaction(self):
        url = reverse('transaction-list')
        data = {'user': self.user.id, 'asset': self.asset.id, 'action': 'buy', 'quantity': '1.00', 'price': '50000.00', 'status': 'completed'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_create_post(self):
        url = reverse('post-list')
        data = {'user': self.user.id, 'title': 'Test Post', 'content': 'This is a test post.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class PriceHistoryTests(APITestCase):
    def setUp(self):
        self.asset = Asset.objects.create(name='Bitcoin', symbol='BTC')

    def test_create_price_history(self):
        url = reverse('pricehistory-list')
        data = {'asset': self.asset.id, 'date': '2023-01-01', 'price': '50000.00'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
