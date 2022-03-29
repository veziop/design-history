from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


class PublicUserTest(TestCase):
    """
    Test CustomUser functionality prior to authentication.
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test correctly and successfully creating a new user."""
        payload = {
            'email': 'test@email.com',
            'name': 'John Doe',
            'password': 'testpass123'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        # Firstly test that the object was created in the serverside
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Now obtain data from the serverside for comparison
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)
        self.assertEqual(payload['email'], response.data['email'])
        self.assertEqual(payload['name'], response.data['name'])

    def test_creating_duplicate_user(self):
        """Test creating a user with identical credentials returns an error."""
        payload = {
            'email': 'test@email.com',
            'name': 'John Doe',
            'password': 'testpass123'
        }
        # Create user with the defined payload
        self.client.post(CREATE_USER_URL, payload)

        # Now attempt to create another user with the same payload and capture the response
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_minimum_length(self):
        """Test that the password intended for user creation is longer than 8 characters"""
        payload = {
            'email': 'test@email.com',
            'name': 'John Doe',
            'password': 'short1'
        }
        # Capture the response from the user creation attempt
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Lookup if the user exists in the serverside
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_password_is_alphanumeric(self):
        """
        Test that the password contains at least one letter character
        and one number character
        """
        payload = {
            'email': 'test@email.com',
            'name': 'John Doe',
            'password': 'abcdefghijk'
        }
        # Capture the response from the user creation attempt
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Lookup if the user exists in the serverside
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
