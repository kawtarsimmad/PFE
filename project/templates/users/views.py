from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
# Create your views here.
from django.views.generic import TemplateView 
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect,render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from users.models import User ###########
from .models import Admin, Donor, Association ###########
#from paypal.standard.forms import PayPalPaymentsForm
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
import codecs
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponseForbidden
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import PasswordResetDoneView
from django.core.mail import EmailMessage, send_mail
from project import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from django.contrib import messages



#
class HomeView(TemplateView):
    template_name = 'users/home.html'

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('dashboard_donor')
    else:
        return render(request,'users/activation_failed.html')
    
    
#register en tant que Donor
def DonorSignup(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        telephone = request.POST.get('telephone', None)
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'users/registerdonor.html', {'error': True, 'message': 'Entrez un email valide !'})

        if password != repassword:
            return render(request, 'users/registerdonor.html', {'error': True, 'message': 'Les mots de passe ne correspondent pas ou sont trop courts !'})

        if not name or not email or not password or not repassword:
            return render(request, 'users/registerdonor.html', {'error': True, 'message': 'Veuillez remplir tous les champs nécessaires !'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'users/registerdonor.html', {'error': True, 'message': 'Un utilisateur avec cet email existe déjà !'})
        
        # Hash the password and create a new user
        utilisateur = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        utilisateur.is_donor = True
        utilisateur.is_association = False
        utilisateur.is_admin=False
        utilisateur.is_active = False
        utilisateur.save()
        
        # Create a donor associated with the user
        donor = Donor.objects.create(
            user=utilisateur,
            phone_number=telephone,  
        )
        donor.save()
        
        # Welcome Email
        subject = "Welcome to HopeBloom Login!!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [utilisateur.email]
        message = "Hello " + utilisateur.first_name + "!! \n" + "Welcome to HopeBloom!! \nThank you for visiting our website\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You"        
        send_mail(subject, message,from_email, to_list, fail_silently=True)
        
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ HopeBloom -  Login!!"
        message2 = render_to_string('users/confirm_email.html',{
            
            'name': utilisateur.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(utilisateur.pk)),
            'token': generate_token.make_token(utilisateur)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [utilisateur.email],
        )
        send_mail(email_subject, message2, from_email, to_list, fail_silently=True)

        
        # Authenticate the user
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
        # Redirect to the dashboard
        return redirect(request, 'users/account_activation_email.html')

    return render(request, 'users/registerdonor.html', {'error': False, 'message': ''})

#Login as donor
def DonorSignIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if user.is_donor:
                return redirect('dashboard_donor')
            elif user.is_association:
                return redirect('dashboard_association')
            else:
                return redirect('dashboardAdmin')
    return render(request, 'users/Logindonor.html', {'error': True, 'message': "Mot de passe incorrect ou Utilisateur n'existe pas!"})
 


@login_required(login_url="")
def dashboard_donor(request):
    user = request.user
    donor = Donor.objects.filter(user=user).first()
    return render(request, 'users/dashboard_donor.html', {'donor': donor})


def donors(request):
    user = request.user
    admin = Admin.objects.filter(user=user).first()
    donors=Donor.objects.all()
    context ={
        'admin': admin,
        'donors': donors,
        
    }
    return render (request,'users/donors.html',context)
 


#####################/ Donor /#############################

##################### Association #########################
#register en tant que Association
def AssociationSignup(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        telephone = request.POST.get('telephone', None)
        stat_juridique=request.POST.get('stat_juridique',None)
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'users/registerassociation.html', {'error': True, 'message': 'Entrez un email valide !'})

        if password != repassword:
            return render(request, 'users/registerassociation.html', {'error': True, 'message': 'Les mots de passe ne correspondent pas ou sont trop courts !'})

        if not name or not email or not password or not repassword:
            return render(request, 'users/registerassociation.html', {'error': True, 'message': 'Veuillez remplir tous les champs nécessaires !'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'users/registerassociation.html', {'error': True, 'message': 'Un utilisateur avec cet email existe déjà !'})
        # Hash the password and create a new user
        utilisateur = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        utilisateur.is_association = True
        utilisateur.is_donor=False
        utilisateur.is_admin=False
        utilisateur.save()

        # Create a association associated with the user
        association = Association.objects.create(
            user=utilisateur,
            phone_number=telephone,
            stat_juridique=stat_juridique,  
        )
        association.save()
        # Authenticate the user
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)

        # Redirect to the dashboard
        return redirect('dashboard_association')

    return render(request, 'users/registerassociation.html', {'error': False, 'message': ''})

#Login as association
def AssociationSignIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if user.is_association:
                return redirect('dashboard_association')
            elif user.is_donor:
                return redirect('dashboard_donor')
            else:
                return redirect('dashboardAdmin')
            
        else:
            return redirect('/')  # Rediriger vers une page d'erreur personnalisée ou une autre page
    return render(request, 'users/Loginassociation.html', {'error': True, 'message': "Mot de passe incorrect ou Utilisateur n'existe pas!"})
 


@login_required(login_url="")
def dashboard_association(request):
    user = request.user
    association = Association.objects.filter(user=user).first()
    return render(request, 'users/dashboard_association.html', {'association': association})


def associations(request):
    user = request.user
    admin = Admin.objects.filter(user=user).first()
    associations=Association.objects.all()
    context ={
        'admin': admin,
        'associations':associations,
        
    }
    return render (request,'users/associations.html',context)

#####################/ Association /#############################

###################  admin  ####################
def signupadmin(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        photo = request.FILES.get('image', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
       

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'users/adminregister.html', {'error': True, 'message': 'Entrez un email valide !!!!!'})

        if password != repassword:
            return render(request, 'users/adminregister.html', {'error': True, 'message': 'Les mots de passe ne correspondent pas ou sont trop courts !'})

        if not name or not email or not password or not repassword:
            return render(request, 'users/adminregister.html', {'error': True, 'message': 'Veuillez remplir tous les champs nécessaires !'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'users/adminregister.html', {'error': True, 'message': 'Un utilisateur avec cet email existe déjà !'})

        # Hash the password and create a new user
        utilisateur = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        utilisateur.is_donor = False
        utilisateur.is_association = False
        utilisateur.is_admin=True
        utilisateur.save()


         # Create a admin associated with the user
        admin = Admin.objects.create(
            user=utilisateur,
            
        )
        admin.image=photo
        admin.save()
        # Authenticate the user
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)

        # Redirect to the dashboard
        return redirect('dashboardAdmin')

    return render(request, 'users/adminregister.html', {'error': False, 'message': ''})


@login_required(login_url="")
def dashboardAdmin(request):
    user = request.user
    admin = Admin.objects.filter(user=user).first()
    donors=Donor.objects.all()
    associations=Association.objects.all()

    context = {
        'admin': admin,
        'donors': donors,
        'associations': associations,
    }
    return render(request, 'users/dashboardAdmin.html', context)
###################### / admin  / ##################

#########  se déconnecter ##############
def custom_logout(request):
    print('Logging out {}'.format(request.user))
    logout(request)
    print(request.user)
    return HttpResponseRedirect('/')  #direction  home

####################### Ajouter et modifier users #####################
###### Donor ############
def add_donor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')  # Retrieve the password from the form


        # Create a new user and donor
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        donor = Donor.objects.create(user=user, phone_number=phone_number)

        return redirect('donors')

    return render(request, 'users/add_donor.html')

def update_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        donor.user.first_name = name
        donor.user.email = email
        donor.phone_number = phone_number
        donor.user.save()
        donor.save()

        return redirect('donors')

    return render(request, 'users/update_donor.html', {'donor': donor})

def delete_donor(request, donor_id):
    donor = get_object_or_404(Donor, pk=donor_id)    
    donor.delete()
    return redirect('donors')

##### Association ########################


def add_association(request, association_id=None):
    if association_id:
        association = get_object_or_404(Association, id=association_id)
    else:
        association = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        stat_juridique = request.POST.get('stat_juridique')
        password = request.POST.get('password')  # Retrieve the password from the form


        if association:
            association.user.first_name = name
            association.user.email = email
            association.phone_number = phone_number
            association.stat_juridique = stat_juridique
            association.user.save()
            association.save()
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            association = Association.objects.create(user=user, phone_number=phone_number, stat_juridique=stat_juridique)

        return redirect('associations')

    return render(request, 'users/add_association.html', {'association': association})

def update_association(request, association_id):
    association = get_object_or_404(Association, id=association_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        stat_juridique = request.POST.get('stat_juridique')

        association.user.first_name = name
        association.user.email = email
        association.phone_number = phone_number
        association.stat_juridique = stat_juridique
        association.user.save()
        association.save()

        return redirect('associations')

    return render(request, 'users/update_association.html', {'association': association})

def delete_association(request, association_id):
    association = Association.objects.get(pk=association_id)
    association.delete()
    return redirect('associations')



###################### Password ######################

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    
    success_url = reverse_lazy('password-reset/done')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('DonorSignIn')