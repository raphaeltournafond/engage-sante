from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

def generate_unique_username(last_name, first_name, cache=[]):
    base_username = slugify(f"{last_name[:5]}{first_name[:2]}")
    unique_username = base_username
    num = 1
    while Utilisateur.objects.filter(username=unique_username).exists() or unique_username in cache:
        unique_username = f"{base_username}{num}"
        num += 1
    return unique_username

class Utilisateur(AbstractUser):
    # Champs relatifs a l adresse
    rue = models.CharField(max_length=100)
    cp = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)
    # Utilise pour savoir si cest un medecin
    is_medecin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and not self.username:
            self.username = generate_unique_username(self.last_name, self.first_name)
            if self.is_medecin:
                self.is_staff = True
        super(Utilisateur, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.username