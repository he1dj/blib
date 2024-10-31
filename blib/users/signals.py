from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from blib.user_profiles.models import UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
                