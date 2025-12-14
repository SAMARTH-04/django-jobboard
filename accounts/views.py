# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

