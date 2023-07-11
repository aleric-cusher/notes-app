from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Tag, Color, Note
from .utils import generate_slug

for model in [Tag, Color, Note]:
    @receiver(post_save, sender=model)
    def set_slug(sender, instance, created, **kwargs):
        if created:
            slug = generate_slug()
            while sender.objects.filter(slug=slug).exists():
                slug = generate_slug()
            instance.slug = slug
            instance.save()

# @receiver(post_save, sender=User)
# def create_default_colors_and_tags(sender, instance, created, **kwargs):
#     if created:
#         # Create default colors
#         default_colors = ['Red', 'Blue', 'Green']
#         for color_name in default_colors:
#             Color.objects.create(name=color_name)

#         # Create default tags
#         default_tags = ['Personal', 'Work', 'Important']
#         for tag_name in default_tags:
#             Tag.objects.create(name=tag_name)