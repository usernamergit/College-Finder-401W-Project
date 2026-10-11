from django.shortcuts import get_object_or_404, render
from .models import Resume

def resume_preview(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    return render(request, "resumes/preview.html", {"resume": resume})