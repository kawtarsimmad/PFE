from django.urls import path
from . import views

urlpatterns = [
     path('publication/',views.publication,name='publication'),
    path('publications/',views.publications,name='publications'),

]
