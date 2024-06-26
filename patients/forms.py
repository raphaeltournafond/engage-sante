from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from patients.widgets import Select2Widget
from .models import Utilisateur

BASE_FIELDS = ('last_name', 'first_name', 'email', 'rue', 'cp', 'ville')
CP_BASE_URL = 'https://geo.api.gouv.fr/communes'
CP_SEARCH_PARAM = 'codePostal'
CP_PLACEHOLDER = 'Entrez un code postal'
VILLE_BASE_URL = 'https://geo.api.gouv.fr/communes?fields=codesPostaux&boost=population&limit=5'
VILLE_SEARCH_PARAM = 'nom'
VILLE_PLACEHOLDER = 'Entrez une ville'

class UtilisateurUpdateForm(UserChangeForm):
    rue = forms.CharField(required=True)
    cp = forms.CharField(required=True, widget=Select2Widget(url=CP_BASE_URL, queryParam=CP_SEARCH_PARAM, placeholder=CP_PLACEHOLDER, fillWith='00'))
    ville = forms.CharField(required=True, widget=Select2Widget(url=VILLE_BASE_URL, queryParam=VILLE_SEARCH_PARAM,  placeholder=VILLE_PLACEHOLDER, maxLength=20))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cp'].initial = self.instance.cp
        self.fields['ville'].initial = self.instance.ville

    class Meta:
        model = Utilisateur
        fields = BASE_FIELDS

class CustomUtilisateurCreationForm(UserCreationForm):
    rue = forms.CharField(required=True)
    cp = forms.CharField(required=True, widget=Select2Widget(url=CP_BASE_URL, queryParam=CP_SEARCH_PARAM, placeholder=CP_PLACEHOLDER, fillWith='00'))
    ville = forms.CharField(required=True, widget=Select2Widget(url=VILLE_BASE_URL, queryParam=VILLE_SEARCH_PARAM,  placeholder=VILLE_PLACEHOLDER, maxLength=20))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cp'].initial = self.instance.cp
        self.fields['ville'].initial = self.instance.ville

    class Meta:
        model = Utilisateur
        fields = BASE_FIELDS