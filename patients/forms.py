from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

class CustomUtilisateurCreationForm(UserCreationForm):
    rue = forms.CharField(required=True)
    cp = forms.CharField(required=True)
    ville = forms.CharField(required=True)

    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'rue', 'cp', 'ville')

class PatientCreationForm(CustomUtilisateurCreationForm):
    is_medecin = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput())

    class Meta(CustomUtilisateurCreationForm.Meta):
        fields = CustomUtilisateurCreationForm.Meta.fields + ('is_medecin',)

class MedecinCreationForm(CustomUtilisateurCreationForm):
    is_medecin = forms.BooleanField(initial=True, required=False, widget=forms.HiddenInput())

    class Meta(CustomUtilisateurCreationForm.Meta):
        fields = CustomUtilisateurCreationForm.Meta.fields + ('is_medecin',)