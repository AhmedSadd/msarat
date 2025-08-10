from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class RegistrationAPITest(APITestCase):
    """
    Test suite for the user registration API endpoint.
    """

    def test_register_user_success(self):
        """
        Ensure we can create a new user and a token is returned.
        """
        url = reverse('register') # We named this in our core.urls
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'somepassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(url, data, format='json')

        # Check for a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the user was created in the database
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

        # Check that the response contains user data and a token
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_register_user_missing_fields(self):
        """
        Ensure registration fails if required fields are missing.
        """
        url = reverse('register')
        data = {
            'username': 'testuser2',
            # Missing password and email
        }

        response = self.client.post(url, data, format='json')

        # Check for a bad request response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that no user was created
        self.assertEqual(User.objects.count(), 0)
