# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import User,ApplicantProfile, RecruiterProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from applications.models import Application
from .forms import ApplicantProfileForm, RecruiterProfileForm
from django.shortcuts import get_object_or_404

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
    user = request.user
    context = {}

    if user.role == "seeker":
        applications = Application.objects.filter(applicant=user)

        context.update({
            "total_applications": applications.count(),
            "shortlisted_count": applications.filter(status="shortlisted").count(),
            "rejected_count": applications.filter(status="rejected").count(),
            "recent_applications": applications.order_by("-id")[:5],
        })

    elif user.role == "recruiter":
        jobs = Job.objects.filter(posted_by=user)
        applications = Application.objects.filter(job__posted_by=user)

        context.update({
            "jobs_count": jobs.count(),
            "total_applicants": applications.count(),
            "pending_applications": applications.filter(status="applied").count(),
            "recent_applications": applications.order_by("-id")[:5],
        })

    return render(request, "accounts/dashboard.html", context)


@login_required
def recruiter_profile(request):
    if request.user.role != "recruiter":
        return render(request, "403.html")

    # Active jobs (default manager returns active only)
    jobs = Job.objects.filter(
        posted_by=request.user
    ).prefetch_related("applications")

    # Inactive jobs (use all_objects to fetch soft-deleted entries)
    inactive_jobs = Job.all_objects.filter(
        posted_by=request.user,
        is_active=False
    ).prefetch_related("applications")

    recruiter_profile = RecruiterProfile.objects.filter(
        user=request.user
    ).first()  # safe fetch

    return render(request, "accounts/recruiter_profile.html", {
        "recruiter": request.user,          # existing
        "profile": recruiter_profile,       # NEW
        "jobs": jobs,                        # existing
        "inactive_jobs": inactive_jobs
    })

@login_required
def applicant_profile(request):
    if request.user.role != "seeker":
        return render(request, "403.html")

    applications = Application.objects.filter(
        applicant=request.user
    ).select_related("job")

    applicant_profile = ApplicantProfile.objects.filter(
        user=request.user
    ).first()  # safe fetch

    return render(request, "accounts/applicant_profile.html", {
        "user": request.user,                # existing
        "profile": applicant_profile,        # NEW
        "applications": applications         # existing
    })



@login_required
def edit_profile(request):
    user = request.user

    if user.role == "seeker":
        profile, created = ApplicantProfile.objects.get_or_create(user=user)
        form_class = ApplicantProfileForm
        redirect_url = "accounts:applicant_profile"

    elif user.role == "recruiter":
        profile, created = RecruiterProfile.objects.get_or_create(user=user)
        form_class = RecruiterProfileForm
        redirect_url = "accounts:recruiter_profile"

    else:
        return render(request, "403.html")

    form = form_class(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(redirect_url)

    return render(request, "accounts/edit_profile.html", {
        "form": form
    })
