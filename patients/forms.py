from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

class CustomUtilisateurCreationForm(UserCreationForm):
    rue = forms.CharField(required=True)
    cp = forms.CharField(required=True)
    ville = forms.CharField(required=True)
    is_medecin = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'rue', 'cp', 'ville', 'is_medecin')