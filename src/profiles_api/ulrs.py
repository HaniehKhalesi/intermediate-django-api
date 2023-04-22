from django.urls import path
from .views import HelloAPIView


urlpatterns = [
    path('test_api_view/', HelloAPIView.as_view(), name='test_api_view')
]



