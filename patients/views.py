from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import PatientCreationForm, MedecinCreationForm
from .models import Utilisateur

def liste_patients(request):
    # Filtre les utilisateurs qui ne sont pas médecins
    patients = Utilisateur.objects.filter(is_medecin=False, is_staff=False, is_superuser=False)
    return render(request, 'patients/liste.html', {'patients': patients})

def register_patient(request):
    if request.method == 'POST':
        form = PatientCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = PatientCreationForm()
    return render(request, 'patients/register.html', {'form': form})

def register_medecin(request):
    if request.method == 'POST':
        form = MedecinCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = MedecinCreationForm()
    return render(request, 'patients/register.html', {'form': form})
