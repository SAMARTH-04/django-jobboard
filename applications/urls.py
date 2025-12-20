from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("update-status/<int:app_id>/", views.update_status, name="update_status"),
]
