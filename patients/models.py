from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class Utilisateur(AbstractUser):
    # Champs relatifs a l adresse
    rue = models.CharField(max_length=100)
    cp = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)
    # Utilise pour savoir si cest un medecin
    is_medecin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.generate_unique_username()
            if self.is_medecin:
                self.is_staff = True
        super(Utilisateur, self).save(*args, **kwargs)

    def generate_unique_username(self):
        base_username = slugify(f"{self.last_name[:5]}{self.first_name[:2]}")
        unique_username = base_username
        num = 1
        while Utilisateur.objects.filter(username=unique_username).exists():
            unique_username = f"{base_username}{num}"
            num += 1
        return unique_username
    
    def __str__(self):
        return self.username