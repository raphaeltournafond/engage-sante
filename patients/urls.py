from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.list_patients, name='list_patients'),
    path('modifier/<int:user_id>/', views.update_utilisateur, name='update_utilisateur'),
    path('enregistrer/patient/', views.register_patient, name='register_patient'),
    path('enregistrer/medecin/', views.register_medecin, name='register_medecin'),
]