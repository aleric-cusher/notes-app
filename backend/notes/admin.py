from django.contrib import admin
from .models import Tag, Color, Note

# Register your models here.

admin.site.register(Note)
admin.site.register(Color)
admin.site.register(Tag)