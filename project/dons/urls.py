from django.urls import path
from . import views

urlpatterns = [
    path('don/',views.don,name='don'),
    path('dons/',views.dons,name='dons'),
    path('faire_don/', views.faire_don, name='faire_don'),
    path('succes/', views.succes, name='succes'),
    path('viewDons/', views.viewDons, name='viewDons'),
]
