from django.urls import path
from . import views

urlpatterns = [
    path('register/patient/', views.register_patient, name='register_patient'),
    path('register/medecin/', views.register_medecin, name='register_medecin'),
]