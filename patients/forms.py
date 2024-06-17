from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from patients.widgets import Select2Widget
from .models import Utilisateur

BASE_FIELDS = ('last_name', 'first_name', 'email', 'rue', 'cp', 'ville')
CP_BASE_URL = 'https://geo.api.gouv.fr/communes'
CP_SEARCH_PARAM = 'codePostal'
CP_PLACEHOLDER = 'Entrez un code postal'
VILLE_BASE_URL = 'https://geo.api.gouv.fr/communes?boost=population&limit=5'
VILLE_SEARCH_PARAM = 'nom'
VILLE_PLACEHOLDER = 'Entrez une ville'

class UtilisateurUpdateForm(UserChangeForm):
    rue = forms.CharField(required=True)
    cp = forms.CharField(required=True, widget=Select2Widget(url=CP_BASE_URL, queryParam=CP_SEARCH_PARAM, placeholder=CP_PLACEHOLDER, fillWith='00'))
    ville = forms.CharField(required=True, widget=Select2Widget(url=VILLE_BASE_URL, queryParam=VILLE_SEARCH_PARAM,  placeholder=VILLE_PLACEHOLDER, maxLength=20))

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