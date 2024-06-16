from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur
from .forms import CustomUtilisateurCreationForm

class CustomUserAdmin(UserAdmin):
    custom_fields = ('rue', 'cp', 'ville', 'is_medecin')
    add_form = CustomUtilisateurCreationForm
    form = CustomUtilisateurCreationForm
    model = Utilisateur
    list_display = ('username', 'email') + custom_fields
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': custom_fields}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': custom_fields}),
    )

admin.site.register(Utilisateur, CustomUserAdmin)