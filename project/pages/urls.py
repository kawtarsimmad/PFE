from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.get_nearby_associations, name='get_nearby_associations'),
    # Ajoutez d'autres patterns d'URL au besoin
]