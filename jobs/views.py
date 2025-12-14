from django.shortcuts import render, redirect
from .models import Job
from .decorators import recruiter_required

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
    return render(request, "jobs/list_jobs.html", {"jobs": jobs})




