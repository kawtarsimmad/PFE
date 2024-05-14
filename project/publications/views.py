from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from . models import Publication
from dons.models import Don
from .forms import PublicationForm
from django.http import HttpResponse
from django.http import JsonResponse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from django.core.mail import send_mail
from categories.models import Category
from users.models import Donor

def publication(request):
    if request.method == "POST":
            form=PublicationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('publications')
    else:
        form = PublicationForm()        
    return render(request, 'publications/publication.html', {'form': form})

def publications(request):
    publications = Publication.objects.all()
    dons = Don.objects.all()
    return render(request, 'publications/publications.html', {'publications': publications,'dons':dons,'total_dons_all': total_dons_all})

def publicationIndex(request):
    publications = Publication.objects.order_by('-date')
    return render(request, 'publications/publicationIndex.html', {'publications': publications})



@login_required
def PubDetail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    dons = publication.dons.all()  # Récupérer tous les dons associés à cette publication
    return render(request, 'publications/detail.html', {'publication': publication, 'dons': dons})
 


def PubCreate(request):
    if request.method == "POST":
        form=PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            publication=form.save(commit=False)
            publication.user= request.user
            
            urgent_category = Category.objects.get(name='Urgent')

            if publication.category == urgent_category:
                publication.save()  # Save the publication first
                send_email_alert(publication)  # Then send email alert
            else:
                publication.save()  # Save the publication

            return redirect('PubList')
    else:
        form = PublicationForm()
    return render(request, 'publications/form.html', {'form': form})

#################### send an alert email ############################
def send_email_alert(publication):
    # Retrieve all donors with valid email addresses
    donors = Donor.objects.filter(user__is_donor=True, user__email__isnull=False).exclude(user__email='')
    recipient_list = [donor.user.email for donor in donors]
    site_domain = "http://127.0.0.1:8000/categories/Urgent/"
    # Send email to donors if there are recipients
    if recipient_list:
        subject = f"Urgent Publication: {publication.titre}"
        message = f"Dear donor, a new urgent publication '{publication.titre}' has been posted on our platform. Visit {site_domain} to learn more."
        from_email = settings.EMAIL_HOST_USER

        try:
            send_mail(subject, message, from_email, recipient_list)
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False    
    else:
        return False  


  

@login_required
def PubUpdate(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES, instance=publication)
        user=request.user
        if form.is_valid():
            form.save()
            if user.is_admin:
                  return redirect('publications')
            elif user.is_association:
                 return redirect('PubList')
               
    else:
        form = PublicationForm(instance=publication)
    return render(request, 'publications/form.html', {'form': form})


@login_required
def PubDelete(request, publication_id):
    publication = get_object_or_404(Publication, pk=publication_id)
    user=request.user
    publication.delete()
    if user.is_admin:
            return redirect('publications')
    elif user.is_association:
            return redirect('PubList')
    



#PubList retourne pubs de user connecté
@login_required
def PubList(request):
    publications = Publication.objects.filter(user=request.user)
    return render(request, 'publications/list.html', {'publications': publications})


def dons_associes(request, publication_id):

    publication = Publication.objects.get(id=publication_id)
    dons = Don.objects.filter(publication=publication)
    total_dons = publication.calculate_total_dons()
    total_dons_all = Publication.calculate_total_dons_all()
    
    return render(request, 'publications/dons_associes.html', {'publication': publication, 'dons': dons,'total_dons_all': total_dons_all})

