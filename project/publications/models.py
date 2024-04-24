from django.db import models
from django.utils import timezone

# Create your models here.

class Publication(models.Model):
    id=models.AutoField(primary_key=True)
    titre=models.CharField(max_length=50)
    contenu=models.TextField()
    date=models.DateTimeField(default=timezone.now)
    image=models.ImageField(upload_to='photos/%y/%m/%d')
    montant=models.DecimalField(max_digits=20,decimal_places=2)

def __str__(self) :
        return self.titre 

