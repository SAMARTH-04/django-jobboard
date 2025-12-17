from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .models import Application

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
