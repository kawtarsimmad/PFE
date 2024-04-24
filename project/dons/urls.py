from django.urls import path
from . import views

urlpatterns = [
    path('don/',views.don,name='don'),
    path('dons/',views.dons,name='dons'),
    
]
