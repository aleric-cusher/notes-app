from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes, parser_classes, api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .serializers import UserSerializer


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
def delete_detail(request, username):
    if request.method == 'DELETE':
        user = get_object_or_404(User, username=username)
        if user:
            user.delete()
            return Response(status=202)
        return Response({'detail': 'Not found'}, status=404)
    
    else:
        return Response({'detail': f'{request.method} not allowed.'}, status=405)