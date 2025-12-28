from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ApplicantProfile, RecruiterProfile

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == "seeker":
        ApplicantProfile.objects.create(user=instance)
    elif instance.role == "recruiter":
        RecruiterProfile.objects.create(
            user=instance,
            company_name=f"{instance.username}'s Company"
        )
