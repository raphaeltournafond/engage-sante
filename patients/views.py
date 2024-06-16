from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from .forms import PatientCreationForm, MedecinCreationForm, UtilisateurUpdateForm
from .models import Utilisateur

def list_patients(request):
    # Filtre les utilisateurs qui ne sont pas médecins
    patients = Utilisateur.objects.filter(is_medecin=False, is_staff=False, is_superuser=False)
    return render(request, 'patients/list.html', {'patients': patients})

def update_utilisateur(request, user_id):
    patient = get_object_or_404(Utilisateur, id=user_id)
    if request.method == 'POST':
        form = UtilisateurUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('list_patients')
    else:
        form = UtilisateurUpdateForm(instance=patient)
    return render(request, 'patients/update.html', {'form': form, 'patient': patient})

def delete_utilisateur(request, user_id):
    patient = get_object_or_404(Utilisateur, id=user_id)
    if request.method == 'POST':
        patient.delete()
        return redirect('list_patients')
    return render(request, 'patients/delete.html', {'patient': patient})

def register_patient(request):
    if request.method == 'POST':
        form = PatientCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_patients')
    else:
        form = PatientCreationForm()
    return render(request, 'patients/register.html', {'form': form})

def register_medecin(request):
    if request.method == 'POST':
        form = MedecinCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_patients')
    else:
        form = MedecinCreationForm()
    return render(request, 'patients/register.html', {'form': form})
