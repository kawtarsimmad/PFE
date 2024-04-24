from django.shortcuts import render
from . models import Reclamation

# Create your views here.

def reclamation(request):
    return render(request, 'reclamations/reclamation.html')
def reclamations(request):
    return render(request, 'reclamations/reclamations.html',{'rc':Reclamation.objects.all()})