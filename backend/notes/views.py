from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from .models import Note, Color, Tag
from .serializers import NoteSerializer, NoteCreateUpdateSerializer, ColorSerializer, TagSerializer
from django.db.models import Q
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
        return Response(serializer.data)


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
        serializer.save()
        return Response(serializer.data)
