from django.shortcuts import render
from django.shortcuts import render
from . models import Publication

def publication(request):
    return render(request, 'publications/publication.html')

def publications(request):
    return render(request, 'publications/publications.html',{'pub ':Publication.objects.all()})

