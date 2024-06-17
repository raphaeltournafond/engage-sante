from django.db import models
from patients.models import Utilisateur

class Consultation(models.Model):
    TYPE_CHOICES = [
        ('Visite', 'Visite'),
        ('Suivi', 'Suivi'),
        ('Operation', 'Opération'),
    ]

    patient = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='consultations')
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.nom} - {self.patient.first_name} {self.patient.last_name}"
