from django.db import models
from django.utils import timezone
from users.models import Donor, Association

# Create your models here.


class Reclamation(models.Model):
    RECLAMATION_TYPES = [
        ('Payment', 'Payment Issue'),
        ('Posts', 'Posts Issue'),
        # Add more types as needed
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
        ('Refused', 'Refused'),
        # Add more statuses as needed
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    recl_type = models.CharField(max_length=100, choices=RECLAMATION_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=100, default='Pending')  # Status as a regular field
    created_at = models.DateTimeField(auto_now_add=True)

    