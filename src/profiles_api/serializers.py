from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import generics, permissions, authentication, serializers
from .models import UserProfile, profileFeedItems


class HelloSerializer(serializers.Serializer):
    """ Serializers a name field for test api_view  """
    name = serializers.CharField(max_length=10)


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializers


class CreateTokenView(ObtainAuthToken):
    serializer_class = serializers.AthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = serializers.UserSerializers
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user



class UserProfileSerializer(serializers.ModelSerializer):
    """ serializer for user profile """

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

        def create(self, validated_data):
            user = UserProfile.object.create_user(
                email=validated_data['email'],
                name=validated_data['name'],
                password=validated_data['password']
            )
            return user


class profileFeedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = profileFeedItems
        fields = ('id', 'user', 'text_status', 'date_create')
        extra_kwargs = {'user': {'read_only': True}}


