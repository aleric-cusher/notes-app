from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserProfile
from .permissions import IsOwner
from .serializers import UserSerializer, UserProfileSerializer


class RegisterUser(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            tokens = {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            return Response(tokens, status=201)
        return Response(serializer.errors, status=400)


class CheckUsernameAvailiblity(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if username := request.data.pop('username', None):
            if User.objects.filter(username=username).exists():
                return Response({"detail": "Username taken", "available": False}, status=200)
            return Response({"detail": "Username available", "available": True}, status=200)
        
        return Response({"detail": "Username not specified"}, status=400)


class LoginUser(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.pop('username')
        password = request.data.pop('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            tokens = {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            return Response(tokens, status=200)
        if User.objects.filter(username=username).exists(): # check if username exists in db
            return Response({'detail': 'Wrong password! Ehhh!'}, status=406)
        return Response({'detail': f'Cannot find account with username: {username}.'}, status=404)


class UserDetailView(views.APIView):
    permission_classes = [IsAuthenticated & IsOwner]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)

    def get(self, request):
        user = self.get_object(request.user.id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        # todo: handle for when the user has a profile picture and wants to delete it
        user = self.get_object(request.user.id)
        self.check_object_permissions(request, user)
        profile_fields = [field.name for field in UserProfile._meta.fields]
        # extracting profile from request.data
        profile_data = {field: request.data[field] for field in request.data.keys() if field in profile_fields}

        user_serializer = UserSerializer(user, data=request.data, partial=True, context = {'request': request})
        user_serializer.is_valid(raise_exception=True)
        instance = user_serializer.save()

        if profile_data:
            try:
                profile = UserProfile.objects.get(user=instance)
                profile_serializer = UserProfileSerializer(profile, data=profile_data, partial=True)
                profile_serializer.is_valid(raise_exception=True)
                profile_serializer.save()
            except (UserProfile.DoesNotExist, AttributeError):
                profile = UserProfile.objects.create(user=instance, **profile_data)
        return Response(user_serializer.data)

    def delete(self, request):
        user = self.get_object(request.user.id)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=204)


class PasswordChangeView(views.APIView):
    permission_classes = [IsAuthenticated & IsOwner]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=404)
        
    def post(self, request):
        user = self.get_object(request.user.id)
        self.check_object_permissions(request, user)

        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not current_password or not new_password:
            return Response({'detail': 'Missing data.'}, status=400)
        
        if not user.check_password(current_password):
            return Response({'detail': 'Invalid password'}, status=401)
    
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password changed successfully'}, status=200)
        
        
        

