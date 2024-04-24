from django.shortcuts import render
from . models import Don
# Create your views here.
def don(request):
    return render(request, 'dons/don.html')
def dons(request):
    return render(request, 'dons/dons.html',{'dn':Don.objects.all()})
