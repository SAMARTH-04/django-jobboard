# Create your models here.
from django.db import models
from accounts.models import User


class JobQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def soft_delete(self):
        return self.update(is_active=False)

    def restore(self):
        return self.update(is_active=True)


class ActiveJobManager(models.Manager):
    def get_queryset(self):
        return JobQuerySet(self.model, using=self._db).filter(is_active=True)

    def with_inactive(self):
        return JobQuerySet(self.model, using=self._db)


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Default manager returns only active jobs
    objects = ActiveJobManager()
    # Use `all_objects` to access both active and inactive jobs
    all_objects = JobQuerySet.as_manager()

    def soft_delete(self):
        if self.is_active:
            self.is_active = False
            self.save(update_fields=["is_active"])

    def restore(self):
        if not self.is_active:
            self.is_active = True
            self.save(update_fields=["is_active"])

    def __str__(self):
        return f"{self.title} at {self.company_name}"
