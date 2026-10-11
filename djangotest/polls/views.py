from django.shortcuts import render
from django.conf import settings
import random

from django.http import HttpResponse

def home_view(request):
    things = [x for x in range(1000)]

    random.shuffle(things)

    context = {
        "website_name": "My Awesome App",
        "item_list": things
    }
    return render(request, 'index.html', context)

def index(request):
    return HttpResponse("THis works well")
