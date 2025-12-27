from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Application

@shared_task
def send_status_email(application_id):
    try:
        instance = Application.objects.get(id=application_id)
        if not instance.applicant.email:
            return "No email provided"
        
        subject = f"Application Status Updated: {instance.job.title}"
        message = f"Hello {instance.applicant.username},\n\nYour application status is now: {instance.status}."
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.applicant.email],
            fail_silently=False,
        )
        return f"Email sent to {instance.applicant.email}"
    except Application.DoesNotExist:
        return "Application not found"
