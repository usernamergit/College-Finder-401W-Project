from django.contrib import admin
from .models_brady import Institution, ProgramSnapshot

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("unit_id", "institution_name", "city", "state_code")
    search_fields = ("institution_name", "city")
    list_filter = ("state_code",)