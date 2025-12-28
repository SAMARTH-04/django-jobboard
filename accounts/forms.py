from django import forms
from .models import ApplicantProfile, RecruiterProfile


class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = ApplicantProfile
        fields = ["profile_image", "summary", "skills", "resume"]

        widgets = {
            "summary": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tell something about yourself"
            }),
            "skills": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Python, Django, React"
            }),
        }


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ["company_name", "company_logo", "company_description", "website"]

        widgets = {
            "company_description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe your company"
            }),
            "website": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://company.com"
            }),
        }
