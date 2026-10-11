from django.contrib import admin
from .models import Resume, Education, Experience, Skill

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "title", "owner", "updated_at")
    inlines = [EducationInline, ExperienceInline, SkillInline]