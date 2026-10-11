from django.shortcuts import render

SAMPLE_JOBS = [
    {
        "title": "Software Engineer",
        "company": "University of Rhode Island",
        "location": "Kingston, RI",
        "url": "https://www.uri.edu/",
    },
    {
        "title": "Data Analyst",
        "company": "State of Rhode Island",
        "location": "Providence, RI",
        "url": "https://www.ri.gov/",
    },
    {
        "title": "Academic Advisor",
        "company": "University of Vermont",
        "location": "Burlington, VT",
        "url": "https://www.uvm.edu/",
    },
]

def job_search(request):
    q = request.GET.get("q", "").strip().lower()
    jobs = SAMPLE_JOBS
    if q:
        jobs = [
            job
            for job in SAMPLE_JOBS
            if q in job["title"].lower()
            or q in job["company"].lower()
            or q in job["location"].lower()
        ]
    return render(request, "jobs/search.html", {"q": q, "jobs": jobs})