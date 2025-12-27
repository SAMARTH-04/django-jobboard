from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Application
from django.conf import settings
from .tasks import send_status_email


# @receiver(post_save, sender=Application)
# def application_status_email(sender, instance, created, **kwargs):

#     # Send mail ONLY when status changes (not on create)
#     if not created and instance.applicant.email:

#         subject = f"Application {instance.status.capitalize()}"
#         message = (
#             f"Hello {instance.applicant.username},\n\n"
#             f"Your application for '{instance.job.title}' has been "
#             f"{instance.status.upper()}.\n\n"
#             "Best regards,\nJob Board Team"
#         )

#         send_mail(
#             subject,
#             message,
#             settings.DEFAULT_FROM_EMAIL,
#             [instance.applicant.email],
#             fail_silently=False,
#         )
#         # testing SMTP
#         #     send_mail(
#         #     "SMTP Test",
#         #     "This confirms Gmail SMTP is working.",
#         #     settings.EMAIL_HOST_USER,
#         #     ["forstudies413@gmail.com"],  # ✅ REAL EMAIL
#         #     fail_silently=False,
#         # )

@receiver(post_save, sender=Application)
def application_status_email(sender, instance, created, **kwargs):
    # Skip sending on creation
    if created:
        return

    # Only proceed if applicant email exists
    if instance.applicant.email:
        # Call the Celery task asynchronously
        send_status_email.delay(instance.id)
