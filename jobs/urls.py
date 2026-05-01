from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("post/", views.post_job, name="post_job"),
    path("", views.list_jobs, name="list_jobs"),
    path("<int:job_id>/applicants/", views.job_applicants, name="job_applicants"),
    path("<int:job_id>/delete/", views.delete_job, name="delete_job"),
    path("<int:job_id>/restore/", views.restore_job, name="restore_job"),
]
