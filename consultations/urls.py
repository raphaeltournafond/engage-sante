from django.urls import path
from . import views

urlpatterns = [
    path('consultations/<int:id>/modifier/', views.update_consultation, name='update_consultation'),
]