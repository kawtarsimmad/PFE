from django.urls import path
from .views import HomeView
from .views import custom_logout 
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    # Ajoutez vos patterns d'URL ici
    path('home/', HomeView.as_view() , name="home"),
    path('logout/', custom_logout, name='logout'),


    path('DonorSignup/', views.DonorSignup, name='DonorSignup'),
    path('dashboard_donor/', views.dashboard_donor, name='dashboard_donor'),
    path('DonorSignIn/', views.DonorSignIn, name='DonorSignIn'),


    path('AssociationSignup/', views.AssociationSignup, name='AssociationSignup'),
    path('dashboard_association/', views.dashboard_association, name='dashboard_association'),
    path('AssociationSignIn/', views.AssociationSignIn, name='AssociationSignIn'),


    path('signupadmin/', views.signupadmin, name='signupadmin'),
    path('dashboardAdmin/',views.dashboardAdmin,name='dashboardAdmin'),

    path('donors/',views.donors,name='donors'),
    path('associations/',views.associations,name='associations'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)