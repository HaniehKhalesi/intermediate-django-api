from django.urls import path
from .views import HelloAPIView, TestAPIViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'api_viewset', TestAPIViewSet, basename='api_viewset')
urlpatterns = router.urls

urlpatterns += [
    path('test_api_view/', HelloAPIView.as_view(), name='test_api_view'),
]

