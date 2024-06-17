from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from consultations import views as cons_views

urlpatterns = [
    path('patients/', views.list_patients, name='list_patients'),
    path('patients/<int:user_id>/', views.info_utilisateur, name='info_utilisateur'),
    path('modifier/<int:user_id>/', views.update_utilisateur, name='update_utilisateur'),
    path('supprimer/<int:user_id>/', views.delete_utilisateur, name='delete_utilisateur'),
    path('connexion/', views.CustomLoginView.as_view(), name='login'),
    path('enregistrer/patient/', views.register_patient, name='register_patient'),
    path('enregistrer/medecin/', views.register_medecin, name='register_medecin'),
    path('reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('not_authorized/', views.not_authorized, name='not_authorized'),
    # Consultations
    path('patients/<int:patient_id>/consultations/', cons_views.list_consultation, name='list_consultation'),
    path('patients/<int:patient_id>/consultations/creer/', cons_views.create_consultation, name='create_consultation'),
]