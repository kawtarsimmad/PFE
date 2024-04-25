from django.urls import path
from . import views

urlpatterns = [
    # Ajoutez vos patterns d'URL ici
    path('reclamation/',views.reclamation,name='reclamation'),
    path('reclamations/',views.reclamations,name='reclamations'),
    path('create/', views.create_reclamation, name='create_reclamation'),
    path('view_reclamations/', views.view_reclamations, name='view_reclamations'),
]