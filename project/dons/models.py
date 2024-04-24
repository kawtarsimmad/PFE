from django.db import models
from django.utils import timezone
# Create your models here.
class Don(models.Model):

    #x=[('photo','phone'),]
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    date=models.DateTimeField(default=timezone.now)
    numCpt=models.DecimalField(max_digits=10,decimal_places=2)
    montantDons=models.DecimalField(max_digits=10,decimal_places=4)
    #content=models.TextField()
    #price=models.DecimalField(max_digits=5,decimal_places=2)
    #image=models.ImageField(upload_to='photos/%y/%m/%d')
    #category=models.CharField(max_length=50,null=True,blank=True,choices=x)
    #date=models.DateField(null=True)
    #time=models.TimeField(null=True)
    #creted=models.DateTimeField(null=True)
    
    
    def __str__(self) :
        return self.name
    class Meta:
        #verbose_name = '',
        ordering =['name']
        