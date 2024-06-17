from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from patients.widgets import Select2Widget
from .models import Utilisateur

BASE_FIELDS = ('last_name', 'first_name', 'email', 'rue', 'cp', 'ville')

class UtilisateurUpdateForm(UserChangeForm):
    rue = forms.CharField(required=True)
    cp = forms.CharField(required=True, widget=Select2Widget(url='https://geo.api.gouv.fr/communes', queryParam='codePostal', fillWith='00'))
    ville = forms.CharField(required=True, widget=Select2Widget(url='https://geo.api.gouv.fr/communes?boost=population&limit=5', queryParam='nom', maxLength=20))

    class Meta:
        model = Utilisateur
        fields = BASE_FIELDS

class CustomUtilisateurCreationForm(UserCreationForm):
    rue = forms.CharField(required=True)
    cp = forms.CharField(required=True)
    ville = forms.CharField(required=True)

    class Meta:
        model = Utilisateur
        fields = BASE_FIELDS

class PatientCreationForm(CustomUtilisateurCreationForm):
    is_medecin = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput())

    class Meta(CustomUtilisateurCreationForm.Meta):
        fields = CustomUtilisateurCreationForm.Meta.fields + ('is_medecin',)

class MedecinCreationForm(CustomUtilisateurCreationForm):
    is_medecin = forms.BooleanField(initial=True, required=False, widget=forms.HiddenInput())

    class Meta(CustomUtilisateurCreationForm.Meta):
        fields = CustomUtilisateurCreationForm.Meta.fields + ('is_medecin',)