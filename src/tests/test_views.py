from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from profiles_api.models import profileFeedItems, UserProfile
from profiles_api.serializers import UserProfileSerializer

def create_user_profile(email, name):
    user = UserProfile.object.create(email=email, name=name)
    return user


def url_detail_recipe(recipe_id):
    return reverse('profile:profiles_api-detail', args=[recipe_id])


USER_PROFILE_URL = reverse('profile:profiles_api-list')


class TestViewsUserProfile(TestCase):
    """ Test View for UserProfile Table """

    def setUp(self):
        self.client = Client()

    def test_retrive_user_profile(self):
        create_user_profile('test@test.com', 'Hanieh')
        create_user_profile('admin@admin.com', 'Jalil')

        response = self.client.get(USER_PROFILE_URL)
        user_profile = UserProfile.object.all()
        serializer = UserProfileSerializer(user_profile, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    #
    # def test_create_user(self):
    #     user = UserProfile.object.get(name='jalil')
    #     user_admin = UserProfile.object.get(name='sara')
    #     self.assertEqual(
    #         user.get_full_name(), "jalil")
