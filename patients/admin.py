from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur
from .forms import CustomUtilisateurCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUtilisateurCreationForm
    form = CustomUtilisateurCreationForm
    model = Utilisateur
    list_display = ('username', 'email', 'rue', 'cp', 'ville', 'is_medecin')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rue', 'cp', 'ville', 'is_medecin')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('rue', 'cp', 'ville', 'is_medecin')}),
    )

admin.site.register(Utilisateur, CustomUserAdmin)