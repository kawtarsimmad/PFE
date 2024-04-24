from django.urls import path
from . import views

urlpatterns = [
    # Ajoutez vos patterns d'URL ici
    path('reclamation/',views.reclamation,name='reclamation'),
    path('reclamations/',views.reclamations,name='reclamations'),
]