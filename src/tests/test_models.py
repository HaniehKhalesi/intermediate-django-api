from django.test import TestCase
from profiles_api.models import profileFeedItems, UserProfile


class UserProfileTest(TestCase):
    """ Test module for UserProfile Table """

    def setUp(self):
        UserProfile.object.create(
            email='test@test.com', name='jalil')
        UserProfile.object.create(
            email='admin@admin.com', name='sara', is_active=True, is_staff=True)

    def test_create_user(self):
        user = UserProfile.object.get(name='jalil')
        user_admin = UserProfile.object.get(name='sara')
        self.assertEqual(
            user.get_full_name(), "jalil")
        self.assertEqual(
            user_admin.get_full_name(), "sara")
        self.assertEqual(
            user.get_email(), "test@test.com")
        self.assertEqual(
            user_admin.get_email(), "admin@admin.com")
        self.assertEqual(
            user_admin.is_staff, True)


class ProfileFeedItemsTest(TestCase):
    """ Test module for profile_feed_items Table """

    def setUp(self):
        user = UserProfile.object.create(email='test1@test.com', name='jalil')
        admin = UserProfile.object.create(email='admin1@admin.com', name='sara', is_staff=True)

        profileFeedItems.objects.create(user=user, text_status="Hi i am Jalil")
        profileFeedItems.objects.create(user=admin, text_status="Hi i am sara")

    def test_create_user(self):
        user_feed_item = profileFeedItems.objects.get(user_id=UserProfile.object.get(name="jalil"))
        admin_feed_item = profileFeedItems.objects.get(user_id=UserProfile.object.get(name="sara"))

        self.assertEqual(
            user_feed_item.get_text_status(), "jalil Hi i am Jalil")
        self.assertEqual(
            admin_feed_item.get_text_status(), "sara Hi i am sara")

