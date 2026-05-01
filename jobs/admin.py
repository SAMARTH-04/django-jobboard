from django.contrib import admin
from .models import Job


@admin.action(description="Restore selected jobs")
def restore_jobs(modeladmin, request, queryset):
	queryset.update(is_active=True)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
	list_display = ("title", "company_name", "posted_by", "is_active", "created_at")
	list_filter = ("is_active", "company_name")
	search_fields = ("title", "company_name", "posted_by__username")
	actions = [restore_jobs]
