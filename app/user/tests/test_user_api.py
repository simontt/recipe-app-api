from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Test client to make requests to API and test response
from rest_framework.test import APIClient
# Module contains some status codes in human readable form (OK instead of 200)
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


# Unauthenticated services, hence public (such as create user)
class PublicUserApiTests(TestCase):
    """Test the users API (public)."""

    def setUp(self):
        # One client to use for all tests instead of always repeating this
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful."""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'John Doe'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test that the object is actually created
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        # We don't want password to be returned in request (security)
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails."""
        payload = {'email': 'test@londonappdev.com',
                   'password': 'testpass',
                   'name': 'Test'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters."""
        payload = {'email': 'test@londonappdev.com',
                   'password': 'pw',
                   'name': 'Test'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Now check that the user was never created
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user."""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given."""
        create_user(email='test@londonappdev.com', password='testpass')
        payload = {'email': 'test@londonappdev.com', 'password': 'wrongpass'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user(self):
        """Test that token is not created if user does not exist."""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required."""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


