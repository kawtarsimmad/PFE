from django.shortcuts import render,redirect
from . models import Don
from .forms import PaiementForm
#from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

def don(request):
    return render(request, 'dons/don.html')
def dons(request):
    return render(request, 'dons/dons.html',{'dn':Don.objects.all()})

def faire_don(request):
    #if request.user.has_perm('your_app_name.can_make_donation'):#
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            montantDons = form.cleaned_data['montantDons']
            don = Don.objects.create(user=request.user, montantDons = montantDons)
            # Ici, vous pourriez rediriger vers un service de paiement tiers
            # ou intégrer directement le processus de paiement ici.
            don.est_paye = True  # Pour cet exemple, nous supposons que le don est payé immédiatement.
            don.save()
            return redirect('viewDons')
    else:
        form = PaiementForm()
    return render(request, 'dons/faire_don.html', {'form': form})


def succes(request):
    return render(request, 'dons/succes.html')



def viewDons(request):
    dons = Don.objects.filter(user=request.user)
    return render(request, 'dons/viewDons.html', {'dons': dons})

