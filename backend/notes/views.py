from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from .models import Note, Color, Tag
from .serializers import NoteSerializer, NoteCreateUpdateSerializer, ColorSerializer, TagSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
import json
import base64


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
        return Response(serializer.data, status=201)


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
        return Response(serializer.data, status=201)


class NoteListCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
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

    def get_and_filter(self, encoded_filters):
        try:
            decoded = base64.b64decode(encoded_filters)
        except:
            return {'detail': 'Query param decode error, please check param'}, 400
        try:
            filters = json.loads(decoded)
        except:
            return {'detail': 'Query param json decode error, please check param'}, 400

        created_to = filters.get('created', {}).get('to')
        created_from = filters.get('created', {}).get('from')
        modified_to = filters.get('modified', {}).get('to')
        modified_from = filters.get('modified', {}).get('from')
        colors = filters.get('colors', [])
        tags = filters.get('tags', [])

        filter_conditions = Q()

        if created_to:
                filter_conditions &= Q(created__lte=created_to)
        if created_from:
                filter_conditions &= Q(created__gte=created_from)
        if modified_to:
                filter_conditions &= Q(modified__lte=modified_to)
        if modified_from:
                filter_conditions &= Q(modified__gte=modified_from)
        if colors:
                filter_conditions &= Q(color__slug__in=colors)
        if tags:
                filter_conditions &= Q(tags__slug__in=tags)
        
        notes = Note.objects.filter(filter_conditions, user=self.request.user)
        notes.prefetch_related('color', 'tags')

        return notes, None
    
    def get(self, request):
        if filters := request.query_params.get('filters'):
            ret, code = self.get_and_filter(filters)
            if code:
                return Response(ret, status=code)
            notes = ret
        else:
            notes = self.get_queryset()

        if order_by := request.query_params.get('order_by'):
            if order_by == 'modified_at':
                notes = notes.order_by('-modified_at')
        else:
            notes = notes.order_by('-created_at')

        serializer = self.get_serializer(notes, many=True)
        paginated = self.get_paginated_response(self.paginate_queryset(serializer.data))
        return paginated

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(NoteSerializer(instance, context={'request': request}).data, status=201)


class TagDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    
    def get_serializer(self, *args, **kwargs):
        serzer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serzer_class(*args, **kwargs)

    def get_queryset(self, slug):
        tag = get_object_or_404(Tag, user=self.request.user, slug=slug)
        return tag
    
    def get(self, request, slug):
        tag = self.get_queryset(slug)
        serializer = self.get_serializer(tag)
        return Response(serializer.data)
    
    def put(self, request, slug):
        tag = self.get_queryset(slug)
        serializer = self.get_serializer(tag, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, slug):
        tag = self.get_queryset(slug)
        tag.delete()
        return Response(status=204)


class ColorDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ColorSerializer
    
    def get_serializer(self, *args, **kwargs):
        serzer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serzer_class(*args, **kwargs)

    def get_queryset(self, slug):
        color = get_object_or_404(Color, user=self.request.user, slug=slug)
        return color
    
    def get(self, request, slug):
        color = self.get_queryset(slug)
        serializer = self.get_serializer(color)
        return Response(serializer.data)
    
    def put(self, request, slug):
        color = self.get_queryset(slug)
        serializer = self.get_serializer(color, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, slug):
        color = self.get_queryset(slug)
        color.delete()
        return Response(status=204)


class NoteDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return NoteCreateUpdateSerializer
        return NoteSerializer
    
    def get_serializer(self, *args, **kwargs):
        serzer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serzer_class(*args, **kwargs)

    def get_queryset(self, slug):
        note = get_object_or_404(Note, user=self.request.user, slug=slug)
        return note
    
    def get(self, request, slug):
        note = self.get_queryset(slug)
        serializer = self.get_serializer(note)
        return Response(serializer.data)
    
    def put(self, request, slug):
        note = self.get_queryset(slug)
        serializer = self.get_serializer(note, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(NoteSerializer(instance, context={'request': request}).data)
    
    def delete(self, request, slug):
        note = self.get_queryset(slug)
        note.delete()
        return Response(status=204)

