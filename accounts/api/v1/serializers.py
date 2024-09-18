from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from accounts.models import User, Profile
from django.core import exceptions
from rest_framework.authtoken.serializers import AuthTokenSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password1']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'detail': 'passwords doesnt match'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password1', None)
        return User.objects.create_user(**validated_data)
        # return super().create(validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):

        if attrs.get('new_password') != attrs.get('new_password1'):
            raise serializers.ValidationError({'detail': 'passwords doesnt match'})
        try:
            validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'description', 'image']
        read_only_fields = ['user']


class CustomAuthTokenSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        user_dict = super().validate(attrs)
        # user_dict = {'username': 'admin@admin.com', 'password': '1380716z', 'user': <User: admin@admin.com>}
        user = User.objects.get(email=user_dict['username'])

        # بررسی فیلد is_verified
        if not user.is_verified:
            raise serializers.ValidationError("This account is not verified.")

        # returning the user object, so it can be accessed later in the view
        attrs['user'] = user
        return attrs
