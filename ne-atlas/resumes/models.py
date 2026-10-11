from django.conf import settings
from django.db import models

class Resume(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resumes",
    )
    title = models.CharField(max_length=200, default="My Resume")
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    summary = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} — {self.title}"

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="education")
    school = models.CharField(max_length=255)
    credential = models.CharField(max_length=255, blank=True)
    start_year = models.CharField(max_length=10, blank=True)
    end_year = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.school

class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="experience")
    role = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    start_year = models.CharField(max_length=10, blank=True)
    end_year = models.CharField(max_length=10, blank=True)
    bullets = models.TextField(blank=True, help_text="One accomplishment per line")

    def __str__(self):
        return f"{self.role} at {self.organization}"

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name