from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User, Profile
from .serializers import RegistrationSerializer, ChangePasswordSerializer, ProfileSerializer, CustomAuthTokenSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'verify': 'check your email to confirm your account'
            }
            user_obj = get_object_or_404(User, email=serializer.validated_data['email'])
            token = self.get_tokens_for_user(user_obj)
            subject = 'verify wiyh email. Click on the link below'
            message = f'http://127.0.0.1:8000/accounts/api/v1/activication/confirm/{token}'
            send_mail(subject, message, 'zeynabdavoudi3@gmail.com',
                      [serializer.validated_data['email']], fail_silently=False)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # create token for user
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ChangePasswordApiView(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            login(request, user)
            return Response({'detail': 'password change successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Profile.objects.all()


class CustomAuthToken(generics.GenericAPIView):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": "Login successful!"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        print(token)
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get('user_id')
        except ExpiredSignatureError:
            return Response({'detail': 'token has been expired'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({'detail': 'token is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return  Response({'detail': 'your account has been already verified'})
        user_obj.is_verified = True
        user_obj.save()
        return Response({'detail': 'your account have been verified and activate successfully'})
