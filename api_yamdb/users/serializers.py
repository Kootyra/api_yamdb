from rest_framework import serializers

from .models import ConfCode, User


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class UserConfirmationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = ConfCode
        fields = ('username', 'confirmation_code')


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        read_only_fields = ('role',)


class NewUserAdmin(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
