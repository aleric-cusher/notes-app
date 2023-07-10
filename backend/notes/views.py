from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from .models import Note, Color, Tag
from .serializers import NoteSerializer, NoteCreateUpdateSerializer, ColorSerializer, TagSerializer

class ColorListCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ColorSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        colors = Color.objects.filter(user=self.request.user)
        return colors
    
    def get_serializer(self, *args, **kwargs):
        serzer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serzer_class(*args, **kwargs)

    def get(self, request):
        colors = self.get_queryset()
        serializer = self.get_serializer(colors, many=True)
        paginated = self.get_paginated_response(self.paginate_queryset(serializer.data))
        return paginated

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TagListCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        tags = Tag.objects.filter(user=self.request.user)
        return tags
    
    def get_serializer(self, *args, **kwargs):
        serzer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serzer_class(*args, **kwargs)

    def get(self, request):
        tags = self.get_queryset()
        serializer = self.get_serializer(tags, many=True)
        paginated = self.get_paginated_response(self.paginate_queryset(serializer.data))
        return paginated

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class NoteListCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        notes = Note.objects.filter(user=self.request.user)
        notes = notes.prefetch_related('tags', 'color')
        return notes
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NoteCreateUpdateSerializer
        return NoteSerializer
    
    def get_serializer(self, *args, **kwargs):
        serzer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serzer_class(*args, **kwargs)

    def get(self, request):
        notes = self.get_queryset()
        serializer = self.get_serializer(notes, many=True)
        paginated = self.get_paginated_response(self.paginate_queryset(serializer.data))
        return paginated

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
