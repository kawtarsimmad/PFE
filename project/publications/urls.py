from django.urls import path
from . import views



urlpatterns = [
    path('publication/',views.publication,name='publication'),
    path('publications/',views.publications,name='publications'),
    path('PubList/',views.PubList,name='PubList'),
    path('detail/<int:pk>/',views.PubDetail,name='detail'),
    path('create/',views.PubCreate,name='create'),
    path('update/<int:pk>/',views.PubUpdate,name='update'),
    path('delete/<int:publication_id>/', views.PubDelete, name='delete'),
    path('checkout/<int:publication_id>/', views.CheckOut, name='checkout'),
    path('payment-success/<int:publication_id>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:publication_id>/', views.paymentFailed, name='payment-failed'),
    path('publicationView/',views.publicationView,name='publicationView'),
    path('publicationIndex/',views.publicationIndex,name='publicationIndex'),


]
