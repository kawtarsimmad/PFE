from django.shortcuts import render
from publications.models import Publication



# Create your views here.
def index(request):
    publications = Publication.objects.all()  # Fetch all publications
    return render(request, 'pages/index.html', {'publications': publications})
