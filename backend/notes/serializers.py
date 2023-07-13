from .models import Color, Tag, Note
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from .utils import create_url


class ColorSerializer(serializers.ModelSerializer):
    # todo: add a hyperlink to notes filtering all the notes for that specific color
    class Meta:
        model = Color
        fields = ['slug', 'color', 'user']
        extra_kwargs = {
            'user': {'write_only': True, 'required': False},
            'slug': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        color = self.Meta.model.objects.create(user=request.user, **validated_data)
        return color

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']
        filter_object = {
            'colors': [instance.slug]
        }
        
        url = create_url(request, filter_object, 'filters', 'notes-list')
        
        representation['url'] = url
        return representation


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['slug', 'name', 'user']
        extra_kwargs = {
            'user': {'write_only': True, 'required': False},
            'slug': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        tag = self.Meta.model.objects.create(user=request.user, **validated_data)
        return tag

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']
        filter_object = {
            'tags': [instance.slug]
        }
        
        url = create_url(request, filter_object, 'filters', 'notes-list')
        
        representation['url'] = url
        return representation


class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    color = ColorSerializer(allow_null=True, required=False)

    class Meta:
        model = Note
        fields = ['slug', 'title', 'content', 'tags', 'color', 'user', 'archived', 'created_at', 'modified_at']
        extra_kwargs = {
            'slug': {'read_only': True},
            'user': {'write_only': True, 'required': False}
        }



class NoteCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )
    color = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Color.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Note
        fields = ['slug', 'title', 'content', 'tags', 'color', 'user', 'archived', 'created_at', 'modified_at']
        read_only_fields = ['slug', 'modified_at', 'created_at']
        extra_kwargs = {
            'slug': {'read_only': True},
            'user': {'write_only': True, 'required': False},
            'archived': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags', None)
        color = validated_data.pop('color', None)
        note = Note.objects.create(user=request.user, **validated_data)
        print(tags, color)

        if tags:
            if tags in Tag.objects.filter(user=request.user):
                note.tags.set(tags)
            else:
                raise NotFound('Tags need to be created before assignment')

        if color:
            if color in Color.objects.filter(user=request.user):
                note.color = color
            else:
                raise NotFound('Color needs to be created before assignment')

        note.save()
        return note
    
    def update(self, instance, validated_data):
        if tags := validated_data.pop('tags', None):
            instance.tags.set(tags)
        if color := validated_data.pop('color', None):
            instance.color = color
        
        return super().update(instance, validated_data)
        
        
        
    
