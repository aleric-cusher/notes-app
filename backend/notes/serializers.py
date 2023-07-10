from .models import Color, Tag, Note
from rest_framework import serializers
from rest_framework.exceptions import NotFound


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
        color = self.Meta.objects.create(user=request.user, **validated_data)
        return color



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


class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    color = ColorSerializer(allow_null=True, required=False)

    class Meta:
        model = Note
        fields = ['slug', 'title', 'content', 'tags', 'color', 'user']
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
        fields = ['slug', 'title', 'content', 'tags', 'color', 'user']
        extra_kwargs = {
            'slug': {'read_only': True},
            'user': {'write_only': True, 'required': False}
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

    