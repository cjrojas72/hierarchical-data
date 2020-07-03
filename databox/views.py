from django.shortcuts import render
from databox.models import File_data

# Create your views here.


def index(request):
    return render(request, "index.html", {"files": File_data.objects.all()})
