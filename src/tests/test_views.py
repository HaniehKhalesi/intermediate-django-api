from django.test import TestCase, Client
from django.urls import reverse

from profiles_api.models import profileFeedItems, UserProfile


class TestViewsUserProfile(TestCase):
    """ Test View for UserProfile Table """

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('')
    #
    # def test_create_user(self):
    #     user = UserProfile.object.get(name='jalil')
    #     user_admin = UserProfile.object.get(name='sara')
    #     self.assertEqual(
    #         user.get_full_name(), "jalil")
