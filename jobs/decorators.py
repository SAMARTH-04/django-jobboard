from django.http import HttpResponseForbidden

def recruiter_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "recruiter":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not allowed to access this page")
    return wrapper
