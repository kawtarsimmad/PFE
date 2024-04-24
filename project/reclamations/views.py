from django.shortcuts import render, redirect
from . models import Reclamation
from django.contrib.auth.decorators import login_required
from .models import Reclamation
from .forms import ReclamationForm


# Create your views here.

def reclamation(request):
    if request.method == "POST":
        form = ReclamationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reclamations')
    else:
        form = ReclamationForm()
    return render(request, 'reclamations/reclamation.html', {'form': form})


def reclamations(request):
    reclamations = Reclamation.objects.all()
    return render(request, 'reclamations/reclamations.html', {'rc': reclamations})

@login_required
def create_reclamation(request):
    if request.method == "POST":
        # Handle form submission to create a new reclamation
        form = ReclamationForm(request.POST)
        if form.is_valid():
            reclamation = form.save(commit=False)
            reclamation.user = request.user
            reclamation.save()
            return redirect('view_reclamations')
    else:
        # Render the reclamation creation form
        form = ReclamationForm()
    return render(request, 'reclamations/create_reclamation.html', {'form': form})


@login_required
def view_reclamations(request):
    reclamations = Reclamation.objects.filter(user=request.user)
    return render(request, 'reclamation/reclamation_list.html', {'reclamations': reclamations})
