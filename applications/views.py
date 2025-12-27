from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .models import Application
from django.contrib import messages

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.role != "seeker":
        return render(request, "403.html")

    if Application.objects.filter(job=job, applicant=request.user).exists():
        return render(request, "applications/already_applied.html")

    if request.method == "POST":
        resume = request.FILES.get("resume")
        Application.objects.create(
            job=job,
            applicant=request.user,
            resume=resume
        )
        return redirect("jobs:list_jobs")

    return render(request, "applications/apply_job.html", {"job": job})

@login_required
def update_status(request, app_id):
    # Only handle POST requests
    if request.method == "POST":
        application = get_object_or_404(Application, id=app_id)

        # Permission check: only the recruiter who posted the job can update
        if request.user != application.job.posted_by:
            return render(request, "403.html")  # or redirect to error page

        # Get new status from form
        status = request.POST.get("status")
        if status in ["applied", "shortlisted", "rejected"]:
            application.status = status
            application.save()  # triggers Celery email task

            messages.success(request, f"Status updated to '{status}' successfully!")

        # Redirect back to the same page
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # If not POST, just redirect
    return redirect("accounts:recruiter_profile")