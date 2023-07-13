from django.urls import path
from .views import (ColorListCreateView,
                    TagListCreateView,
                    NoteListCreateView,
                    TagDetailView,
                    ColorDetailView,
                    NoteDetailView)

urlpatterns = [
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<str:slug>/', TagDetailView.as_view(), name='tag-detail'),

    path('colors/', ColorListCreateView.as_view(), name='color-list-create'),
    path('colors/<str:slug>/', ColorDetailView.as_view(), name='color-detail'),

    path('', NoteListCreateView.as_view(), name='note-list-create'),
    path('<str:slug>/', NoteDetailView.as_view(), name='note-detail'),
]
