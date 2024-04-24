from django.db import models
from django.utils import timezone
from . models import Association, Category

# Create your models here.

class Publication(models.Model):
    id=models.AutoField(primary_key=True)
    titre=models.CharField(max_length=150)
    contenu=models.TextField()
    date=models.DateTimeField(default=timezone.now)
    image=models.ImageField(upload_to='photos/%y/%m/%d')
    montant=models.DecimalField(max_digits=20,decimal_places=2)
    association=models.ForeignKey(Association,on_delete=models.CASCADE,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) :
        return self.titre 
    
    class Meta:
        ordering=['-date']


