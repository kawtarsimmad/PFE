from django.db import models
from django.utils import timezone


# Create your models here.

class Reclamation(models.Model):
     
     id=models.AutoField(primary_key=True)
     contenu=models.TextField()
     date=models.DateTimeField(default=timezone.now)
     #etat=
     
    