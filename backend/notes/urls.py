from django.urls import path
from .views import ColorListCreateView, TagListCreateView, NoteListCreateView

urlpatterns = [
    path('tags/', TagListCreateView.as_view(), name='tags-list'),
    # path('tags/<str:slug>/', , name='tags-detail'),

    path('colors/', ColorListCreateView.as_view(), name='colors-list'),
    # path('colors/<str:slug>/', , name='colors-detail'),

    path('', NoteListCreateView.as_view(), name='notes-list'),
    # path('<str:slug>/', , name='notes-detail'),
]
