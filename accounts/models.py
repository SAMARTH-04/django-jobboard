from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class ApplicantProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="applicant_profile"
    )
    profile_image = models.ImageField(
        upload_to="profiles/applicants/",
        blank=True,
        null=True
    )
    summary = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} - Applicant Profile"


class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="recruiter_profile"
    )
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(
        upload_to="profiles/recruiters/",
        blank=True,
        null=True
    )
    company_description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"
