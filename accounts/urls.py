from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("recruiter/profile/", views.recruiter_profile, name="recruiter_profile"),
    path("applicant/profile/", views.applicant_profile, name="applicant_profile"),

]
