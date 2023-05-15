from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from profiles_api.models import profileFeedItems, UserProfile
from profiles_api.serializers import UserProfileSerializer

def create_user_profile(email, name):
    user = UserProfile.object.create(email=email, name=name)
    return user


def url_detail_recipe(user_id):
    return reverse('profile:profiles_api-detail', args=[user_id])


USER_PROFILE_URL = reverse('profile:profiles_api-list')


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

    def test_create_user_profile(self):
        user = self.user_test
        payload = {
            'email': 'test_create@test2.com',
            'name': 'Ana'
        }

        response = self.client.post(USER_PROFILE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_profile = UserProfile.object.get(id=response.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(user_profile, k), v)
        self.assertEqual(user, user_profile.email)





