from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from .models import User, ConfCode
from .serializers import (UserRegistrationSerializer,
                          UserConfirmationSerializer,
                          UserProfileSerializer)
from django.shortcuts import get_object_or_404
import secrets
import string


def generate_alphanum_crypt_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(length))
    return crypt_rand_string


class UserRegistration(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def signup(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if (not serializer.is_valid()
                or serializer.validated_data['username'] == 'me'):
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        confirmation_code = generate_alphanum_crypt_string(8)
        send_mail(
            'Registration code',
            f'Для получения токена введите код {confirmation_code}',
            'from@example.com',
            [serializer.data.get('email')],
            fail_silently=False,
        )
        name = serializer.data.get('username')
        user = get_object_or_404(User, username=name)
        ConfCode.objects.create(username=user,
                                confirmation_code=confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserConfirmation(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def confirmation(self, request):
        serializer = UserConfirmationSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        print(serializer.data)
        user_form = serializer.data.get('username')
        user_base = get_object_or_404(User, username=user_form)
        code_base = get_object_or_404(ConfCode, username=user_base)
        code_form = serializer.data.get('confirmation_code')
        if code_base.confirmation_code != code_form:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        token = AccessToken.for_user(user_base)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)


class UserProfile(viewsets.ModelViewSet):

    def profile(self, request):
        user = request.user
        serializer = UserProfileSerializer(
            user,
            data=request.data
        )
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
