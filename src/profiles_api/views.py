from rest_framework import filters, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from .models import UserProfile, profileFeedItems
from .serializers import (
    HelloSerializer,
    UserProfileSerializer,
    profileFeedItemsSerializer,
    UserSerializers,
    AthTokenSerializer,
)
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from . import permissions


class HelloAPIView(APIView):
    """Test API VIEW"""

    serializer_class = HelloSerializer

    def get(self, request, format=None):
        """Return a list af API View fe+atures"""
        an_apiview = [
            "Uses HTTP methods as functions (get, post, patch, put, delete)",
            "Is similar to a traditional Django View",
            "Gives you the most control over your logic",
            "Is mapped manually to URLs",
        ]
        return Response({"message": "Hello", "an_apiview": an_apiview})

    def post(self, request):
        """create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get("name")
            message = f"Hello {name}"
            return Response({"name": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handel update on object"""
        return Response({"methode": "put"})

    def patch(self, request, pk=None):
        """Handel a partial update of an object"""
        return Response({"methode": "patch"})

    def delete(self, request, pk=None):
        """Handel a delete of an object"""
        return Response({"methode": "delete"})


# Create ViewSet
class TestAPIViewSet(ViewSet):
    """Test for viewSet"""

    serializer_class = HelloSerializer

    def list(self, request):
        """list in ViewSet equals get result Function"""
        as_viewSet = [
            "message 1",
            "message 2",
            "message 3",
            "message 4",
        ]
        message = "this is list function "
        return Response({"message": message, "as_view": as_viewSet})

    def create(self, request):
        """create in ViewSet equals post in api view"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"
            return Response({"message": message})
        else:
            return Response(
                {"detail": "this input is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None):
        """get a detail item"""
        return Response({"http_method": "GET"})

    def update(self, request, pk=None):
        """update a detail item"""
        return Response({"http_method": "PUT"})

    def partial_update(self, request, pk=None):
        """partial update a detail item"""
        return Response({"http_method": "PATCH"})

    def destroy(self, request, pk=None):
        """delete a detail item"""
        return Response({"http_method": "DELETE"})


# create user profile API
class UserProfileViewSet(ModelViewSet):
    """create update get put delete for profile user"""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.object.all()
    authentication_classes = (TokenAuthentication,)
    # Each user can only update her/his own profile
    permission_classes = (permissions.UpdateOneProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "email")


# Login API
class UserLoginAPIView(ObtainAuthToken):
    """Handel Create user authentication token"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFreedItemView(ModelViewSet):
    """view for show text status and edit by only user create"""

    serializer_class = profileFeedItemsSerializer
    queryset = profileFeedItems.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.profileFreeItem_permissions,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializers


class CreateTokenView(ObtainAuthToken):
    serializer_class = AthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
