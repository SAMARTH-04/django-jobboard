from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Application

@receiver(post_save, sender=Application)
def application_status_email(sender, instance, created, **kwargs):
    if not created:
        send_mail(
            subject=f"Application {instance.status.capitalize()}",
            message=f"Your application for {instance.job.title} is {instance.status}.",
            from_email="noreply@jobboard.com",
            recipient_list=[instance.applicant.email],
            fail_silently=True,
        )
