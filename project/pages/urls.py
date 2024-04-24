from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Ajoutez d'autres patterns d'URL au besoin
]