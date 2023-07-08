from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['name'] = user.first_name
        return token


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'date_joined']
        read_only_fields = ['date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = make_password(validated_data.pop('password'))
        user = User.objects.create(password=password, **validated_data)
        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        profile_fields = [field.name for field in UserProfile._meta.fields]
        profile_fields.remove('user')
        try:
            profile = UserProfile.objects.get(user=instance).__dict__
            for field in profile_fields:
                representation[field] = profile[field]
            return representation
        except UserProfile.DoesNotExist:
            return representation