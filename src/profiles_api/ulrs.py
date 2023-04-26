from django.urls import path, include
from .views import HelloAPIView, TestAPIViewSet, UserProfileViewSet, UserLoginAPIView, UserProfileFreedItemView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'api_viewset', TestAPIViewSet, basename='api_viewset')
router.register(r'profiles_api', UserProfileViewSet, basename='profiles_api')
router.register('profile_feed', UserProfileFreedItemView)

urlpatterns = [
    path('test_api_view/', HelloAPIView.as_view(), name='test_api_view'),
    path('', include(router.urls)),
    path('login/', UserLoginAPIView.as_view()),
]

