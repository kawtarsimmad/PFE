from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from . models import Publication
from .forms import PublicationForm
from django.http import HttpResponse
from django.http import JsonResponse


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
    return render(request, 'publications/publications.html', {'publications': publications})




@login_required
def PubDetail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, 'publications/detail.html', {'publication': publication})
 


def PubCreate(request):
    if request.method == "POST":
        form=PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            publication=form.save(commit=False)
            publication.user= request.user
            publication.save()
            return redirect('PubList')
    else:
        form = PublicationForm()
    return render(request, 'publications/form.html', {'form': form})

  

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

