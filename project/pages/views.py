from django.shortcuts import render
from publications.models import Publication
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from users.models import Association



# Create your views here.
def index(request):
    publications = Publication.objects.all()  # Fetch all publications
    return render(request, 'pages/index.html', {'publications': publications})


