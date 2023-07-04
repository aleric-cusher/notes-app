from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.contrib.auth import authenticate
from rest_framework.decorators import permission_classes, parser_classes, api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

# Set proper permission calasses

@permission_classes([AllowAny])
@api_view(['POST'])
def login(request: HttpRequest):
    username = request.data.pop('username')
    password = request.data.pop('password')
    user = authenticate(username, password)

    if user:
        refresh = RefreshToken.for_user(user)
        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        return Response(data, status=200)
    if User.objects.filter(username=username).exists(): # check if username exists in db
        return Response({'detail': 'Wrong password! Ehhh!'}, status=406)
    return Response({'detail': f'Cannot find {username}.'}, status=404)


@permission_classes([AllowAny])
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@permission_classes([AllowAny])
@api_view(['DELETE'])
def user_detail(request, username):
    if request.method == 'DELETE':
        user = get_object_or_404(User, username=username)
        if user:
            user.delete()
            return Response(status=202)
        return Response({'detail': 'Not found'}, status=404)
    
    else:
        return Response({'detail': f'{request.method} not allowed.'}, status=405)
    

@permission_classes([AllowAny])
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    if users:
        return Response(users, status=200)
    return Response({'detail': 'Not found.'}, status=404)