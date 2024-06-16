from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    # Champs relatifs a l adresse
    rue = models.CharField(max_length=100)
    cp = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)
    # Utilise pour savoir si cest un medecin
    is_medecin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_medecin:
            self.is_staff = True
        super(Utilisateur, self).save(*args, **kwargs)