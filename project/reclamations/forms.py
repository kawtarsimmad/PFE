# forms.py
from django import forms
from .models import Reclamation

class ReclamationForm(forms.ModelForm):
    recl_type= forms.ChoiceField(choices=Reclamation.RECLAMATION_TYPES, widget=forms.Select(attrs={"class":"forms-control", "placeholder": "recl_type"}))
    description= forms.CharField(widget=forms.Textarea(attrs={"class":"forms-control", "placeholder": "description"}))
    status=forms.CharField(widget=forms.TextInput(attrs={"class":"forms-control", "placeholder": "status"}))
    
    class Meta:
            model = Reclamation
            fields = ['recl_type', 'description', 'status']
