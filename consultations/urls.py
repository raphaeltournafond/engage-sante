from django.urls import path
from . import views

urlpatterns = [
    path('consultations/<int:id>/modifier/', views.update_consultation, name='update_consultation'),
    path('consultations/<int:id>/supprimer/', views.delete_consultation, name='delete_consultation'),
]