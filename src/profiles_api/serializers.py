from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import UserProfile, profileFeedItems
from django.utils.translation import gettext as _


class HelloSerializer(serializers.Serializer):
    """Serializers a name field for test api_view"""

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """serializer for user profile"""

    class Meta:
        model = UserProfile
        fields = ("id", "email", "name", "password")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

        def create(self, validated_data):
            user = UserProfile.object.create_user(
                email=validated_data["email"],
                name=validated_data["name"],
                password=validated_data["password"],
            )
            return user


class profileFeedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = profileFeedItems
        fields = ("id", "user", "text_status", "date_create")
        extra_kwargs = {"user": {"read_only": True}}


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().object.create_user(**validated_data)

    # def update(self,instance, validate_data):
    #     password = validate_data.pop('password', None)
    #     user = super().update(instance, validate_data)
    #     if password:
    #         user.set_password(password)
    #         user.save()
    #     return user

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = _("unable create token ")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
