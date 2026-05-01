from django.shortcuts import render, redirect
from .models import Job
from .decorators import recruiter_required
from applications.models import Application
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@recruiter_required
def post_job(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        company_name = request.POST.get("company_name")
        location = request.POST.get("location")

        Job.objects.create(
            title=title,
            description=description,
            company_name=company_name,
            location=location,
            posted_by=request.user
        )
        return redirect("jobs:list_jobs")

    return render(request, "jobs/post_job.html")


def list_jobs(request):
    jobs = Job.objects.all().order_by("-created_at")
    paginator = Paginator(jobs, 5)

    page = request.GET.get("page")
    jobs = paginator.get_page(page)

    return render(request, "jobs/list_jobs.html", {"jobs": jobs})



def job_applicants(request, job_id):
    # use all_objects to allow viewing applicants for inactive jobs by owner
    job = Job.all_objects.get(id=job_id)

    if request.user != job.posted_by:
        return render(request, "403.html")

    applications = job.applications.select_related("applicant")
    return render(request, "jobs/applicants.html", {
        "job": job,
        "applications": applications
    })



@login_required
@recruiter_required
@require_POST
def delete_job(request, job_id):
    job = get_object_or_404(Job.all_objects, id=job_id)

    if request.user != job.posted_by:
        return render(request, "403.html")

    job.soft_delete()
    return redirect("accounts:recruiter_profile")


@login_required
@recruiter_required
@require_POST
def restore_job(request, job_id):
    job = get_object_or_404(Job.all_objects, id=job_id)

    if request.user != job.posted_by:
        return render(request, "403.html")

    job.restore()
    return redirect("accounts:recruiter_profile")





