from rest_framework import serializers

from .models import User, ConfCode


class UserRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email') 

class UserConfirmationSerializer(serializers.ModelSerializer):     
    username = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = ConfCode
        fields = ('username', 'confirmation_code') 

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',)