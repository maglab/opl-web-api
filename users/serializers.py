from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, Contact


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["firebase_uuid", "role", "affiliation"]


# This serializer creates the user profile at the end if it is populated.
class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ["username", "password", "email", "profile"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        user = User.objects.create_user(**validated_data)
        if profile_data:
            UserProfile.objects.get_or_create(account=user, **profile_data)
        return user


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
