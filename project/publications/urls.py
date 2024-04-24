from django.urls import path
from . import views
from .views import PubList,PubDetail,PubCreate,PubUpdate,PubDelete

urlpatterns = [
    path('publication/',views.publication,name='publication'),
    path('publications/',views.publications,name='publications'),
    path('list/',PubList.as_view(),name='list'),
    path('detail/<int:pk>/',PubDetail.as_view(),name='detail'),
    path('create/',PubCreate.as_view(),name='create'),
    path('update/<int:pk>/',PubUpdate.as_view(),name='update'),
    path('delete/<int:pk>/',PubDelete.as_view(),name='delete'),


]
