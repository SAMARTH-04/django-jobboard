# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from applications.models import Application

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("accounts:signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        login(request, user)
        return redirect("accounts:dashboard")  # we’ll create this later

    return render(request, "accounts/signup.html")

    

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")

@login_required
def recruiter_profile(request):
    if request.user.role != "recruiter":
        return render(request, "403.html")

    jobs = Job.objects.filter(posted_by=request.user).prefetch_related("applications")

    return render(request, "accounts/recruiter_profile.html", {
        "recruiter": request.user,
        "jobs": jobs
    })

@login_required
def applicant_profile(request):
    if request.user.role != "seeker":
        return render(request, "403.html")

    applications = Application.objects.filter(applicant=request.user).select_related("job")

    return render(request, "accounts/applicant_profile.html", {
        "user": request.user,
        "applications": applications
    })

