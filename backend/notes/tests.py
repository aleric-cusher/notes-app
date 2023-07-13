from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Note, Tag, Color
from .serializers import NoteSerializer, TagSerializer, ColorSerializer

class TagListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        Tag.objects.create(slug='tag-1', name='Tag 1', user=self.user)
        Tag.objects.create(slug='tag-2', name='Tag 2', user=self.user)
        
    def test_get_tags(self):
        url = reverse('tag-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_create_tag(self):
        url = reverse('tag-list-create')
        data = {
            'name': 'New Tag'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(Tag.objects.last().name, 'New Tag')


class NoteListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # Creating sample data
        self.color = Color.objects.create(color='#ffffff', user=self.user)
        self.tag1 = Tag.objects.create(name='Tag 1', user=self.user)
        self.tag2 = Tag.objects.create(name='Tag 2', user=self.user)
        
    def test_create_note(self):
        url = reverse('note-list-create')
        data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
            'color': self.color.slug,
            'tags': [self.tag1.slug, self.tag2.slug]
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, data)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.first().title, 'Test Note')
        self.assertEqual(Note.objects.first().content, 'This is a test note.')
        self.assertEqual(Note.objects.first().color, self.color)
        self.assertEqual(list(Note.objects.first().tags.all()), [self.tag1, self.tag2])
        
    def test_get_notes(self):
        # Creating sample notes
        Note.objects.create(title='Note 1', content='Content 1', color=self.color, user=self.user)
        Note.objects.create(title='Note 2', content='Content 2', color=self.color, user=self.user)
        
        url = reverse('note-list-create')
        response = self.client.get(url)
        results = response.data['results']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 2, response.data)
        self.assertEqual(results[0]['title'], 'Note 1')
        self.assertEqual(results[1]['title'], 'Note 2')
        
    def test_create_note_unauthenticated(self):
        self.client.force_authenticate(user=None)
        
        url = reverse('note-list-create')
        data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
            'color': self.color.slug,
            'tags': [self.tag1.slug, self.tag2.slug]
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Note.objects.count(), 0)

