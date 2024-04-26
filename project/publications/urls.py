from django.urls import path
from . import views
from .views import PubList,PubCreate,PubDetail,PubUpdate,PubDelete

urlpatterns = [
    path('publication/',views.publication,name='publication'),
    path('publications/',views.publications,name='publications'),
    path('PubList/',views.PubList,name='PubList'),
    path('detail/<int:pk>/',views.PubDetail,name='detail'),
    path('create/',views.PubCreate,name='create'),
    path('update/<int:pk>/',views.PubUpdate,name='update'),
    path('delete/<int:pk>/',views.PubDelete,name='delete'),


]
