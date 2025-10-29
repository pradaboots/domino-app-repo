# api/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

@receiver(post_save, sender=User, dispatch_uid="create_profile_once")
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User, dispatch_uid="save_profile_once")
def save_user_profile(sender, instance, **kwargs):
    # Ensure profile exists and stays in sync (optional safety)
    UserProfile.objects.get_or_create(user=instance)
    instance.profile.save()
