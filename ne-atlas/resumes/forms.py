from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["title", "full_name", "email", "phone", "summary"]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 4}),
        }