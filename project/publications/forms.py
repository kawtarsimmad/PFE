from django import forms
from .models import Publication

class CRUDPUBFORM(forms.ModelForm):
    titre=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control",'placeholder':'titre'}))
    contenu=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control",'placeholder':'contenu'}))
    image=forms.ImageField()
    montant=forms.DecimalField()
   
    class Meta:
        fields=['titre','contenu','image','montant']