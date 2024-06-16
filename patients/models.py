from django.db import models
from django.contrib.auth.models import User

# Modeles utilisateurs etendus du modele de base avec l adresse complete
class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Champs relatifs a l adresse
    rue = models.CharField(max_length=100)
    cp = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username

class Patient(Utilisateur):

    def save(self, *args, **kwargs):
        self.user.is_staff = False
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient: {self.user.username}"

class Medecin(Utilisateur):
    
    def save(self, *args, **kwargs):
        self.user.is_staff = True
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Medecin: {self.user.username}"
