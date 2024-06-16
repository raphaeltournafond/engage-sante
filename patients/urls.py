from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.liste_patients, name='liste_patients'),
    path('register/patient/', views.register_patient, name='register_patient'),
    path('register/medecin/', views.register_medecin, name='register_medecin'),
]