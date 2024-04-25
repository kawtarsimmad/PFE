from django.shortcuts import render
from . models import Publication
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse,reverse_lazy
from .forms import CRUDPUBFORM


def publication(request):
    return render(request, 'publications/publication.html')

def publications(request):
    return render(request, 'publications/publications.html',{'pub ':Publication.objects.all()})

class PubList(ListView):

    model = Publication
    context_object_name= 'publications'
    template_name = 'publications/list.html'

class PubDetail(DetailView):
    model = Publication
    context_object_name= 'publications'
    template_name = 'publications/detail.html'
 
class PubCreate(CreateView):
    model = Publication
    form_class=CRUDPUBFORM
    template_name = 'publications/form.html'
    success_url= reverse_lazy('publications')

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(PubCreate, self).form_valid(form)
    
class PubUpdate(UpdateView):
    model = Publication
    form_class=CRUDPUBFORM
    template_name = 'publications/form.html'
    success_url= reverse_lazy('publications')

    def form_valid(self, form):
        return super(PubUpdate, self).form_valid(form)

class PubDelete(DeleteView):
    model = Publication
    template_name = 'publications/delete.html'

    def get_success_url(self) :
        return reverse('publications')
