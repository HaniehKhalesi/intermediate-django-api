from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from profiles_api.models import profileFeedItems, UserProfile
from profiles_api.serializers import UserProfileSerializer
from rest_framework.test import APIClient


def create_user_profile(email, name):
    user = UserProfile.object.create(email=email, name=name)
    return user


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().object.create_user(**params)


CREATE_USER_URL = reverse('profile:create')
TOKEN_URL = reverse('profile:token')


def url_detail_recipe(user_id):
    return reverse('profile:profiles_api-detail', args=[user_id])


USER_PROFILE_URL = reverse('profile:profiles_api-list')


class PublicUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_success(self):
        payload = {
            'email': 'test@example.com',
            'password': 'sample123',
            'name': 'Test User',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().object.get(email=payload['email'])
        # self.assertTrue(user.check_password(payload['password']))
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short_error(self):
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().object.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        create_user_token = {
            'email': 'tet@example.com',
            'password': 'sample123123',
            'name': 'user token'
        }
        create_user(**create_user_token)

        payload = {
            'email': create_user_token['email'],
            'password': create_user_token['password'],
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentails(self):
        create_user(email='test@example.com', password='goddpass', name='good name')
        payload = {'email': 'test@example.com', 'password': 'baddpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blanke_password(self):
        payload = {'email': 'test@example.com', 'password': 'goddpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class TestViewsUserProfile(TestCase):
    """ Test View for UserProfile Table """

    def setUp(self):
        self.client = Client()
        self.user_test = create_user_profile('user_test@test.com', 'Ana')

    def test_retrive_user_profile(self):
        create_user_profile('test@test.com', 'Hanieh')
        create_user_profile('admin@admin.com', 'Jalil')

        response = self.client.get(USER_PROFILE_URL)
        user_profile = UserProfile.object.all()
        serializer = UserProfileSerializer(user_profile, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_profile_user_with_id(self):
        user = self.user_test
        url = url_detail_recipe(user_id=user.id)
        response = self.client.get(url)
        serializer = UserProfileSerializer(user)
        self.assertEqual(response.data, serializer.data)


