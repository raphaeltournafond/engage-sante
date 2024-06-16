from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import PatientCreationForm, MedecinCreationForm

def register_patient(request):
    if request.method == 'POST':
        form = PatientCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = PatientCreationForm()
    return render(request, 'register.html', {'form': form})

def register_medecin(request):
    if request.method == 'POST':
        form = MedecinCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = MedecinCreationForm()
    return render(request, 'register.html', {'form': form})
