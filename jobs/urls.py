from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("post/", views.post_job, name="post_job"),
    path("", views.list_jobs, name="list_jobs"),
]
