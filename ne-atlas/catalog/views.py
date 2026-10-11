from django.shortcuts import get_object_or_404, render
from .models_brady import Institution, InstitutionSnapshot, ProgramSnapshot

STATES = [
    ("CT", "Connecticut"),
    ("ME", "Maine"),
    ("MA", "Massachusetts"),
    ("NH", "New Hampshire"),
    ("RI", "Rhode Island"),
    ("VT", "Vermont"),
]

TUITION_RANGES = [
    ("0-10000", "Under $10,000"),
    ("10000-20000", "$10,000 – $20,000"),
    ("20000-40000", "$20,000 – $40,000"),
    ("40000-100000", "$40,000 – $100,000"),
]

FIELDS = [
    ("51", "Health / Medical"),
    ("52", "Business"),
    ("11", "Computer and information sciences"),
    ("14", "Engineering"),
    ("13", "Education"),
    ("26", "Biological sciences"),
    ("42", "Psychology"),
]

def home(request):
    state = request.GET.get("state", "").upper()
    tuition = request.GET.get("tuition", "")
    field = request.GET.get("field", "")

    colleges = Institution.objects.order_by("institution_name")
    if state in dict(STATES):
        colleges = colleges.filter(state_code=state)

    if field in dict(FIELDS):
        matched_ids = ProgramSnapshot.objects.filter(
            cip_code__startswith=field
        ).values_list("unit_id", flat=True)
        colleges = colleges.filter(unit_id__in=matched_ids)

    colleges = colleges[:50]
    return render(request, "catalog/home.html", {
        "colleges": colleges,
        "states": STATES,
        "state": state,
        "tuition_ranges": TUITION_RANGES,
        "tuition": tuition,
        "fields": FIELDS,
        "field": field,
    })

def school_detail(request, unit_id):
    college = get_object_or_404(Institution, unit_id=unit_id)
    snapshot = InstitutionSnapshot.objects.filter(unit_id=unit_id).first()
    return render(request, "catalog/detail.html", {
        "college": college,
        "snapshot": snapshot,
    })

def compare(request):
    return render(request, "catalog/compare.html")