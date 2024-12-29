from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import User


class UserRegistrationTest(APITestCase):
    # path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    def setUp(self):
        # Any setup you might need for your tests
        self.url = reverse('user-registration')  # Adjust to your URL name for registration

    def test_register_user(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['user']['email'], 'testuser@example.com')

    def test_register_user_invalid_data(self):
        # Test case where required fields are missing
        data = {
            'username': '',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_saving_user(self):
        # Test data to register the user
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
        }

        # Make a POST request to register the user
        response = self.client.post(self.url, data, format='json')

        # Assert that the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the tokens are returned
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

        # Assert that the user data returned in the response matches the input data
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['user']['email'], 'testuser@example.com')

        # Verify the user is saved in the database
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

        # Verify the password is hashed (don't check for plain text password)
        self.assertTrue(user.check_password('testpassword123'))