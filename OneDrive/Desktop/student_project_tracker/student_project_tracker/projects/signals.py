from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Evaluation


@receiver(post_save, sender=Evaluation)
def notify_coordinator(sender, instance, created, **kwargs):
    if created:
        print("Evaluation submitted")
