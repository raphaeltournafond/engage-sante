from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from consultations.forms import ConsultationForm
from patients.models import Utilisateur
from .models import Consultation

@login_required
def list_consultation(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)
    consultations = utilisateur.consultations.all()
    return render(request, 'consultations/list.html', {'consultations': consultations, 'utilisateur': utilisateur})

@login_required
def create_consultation(request, user_id):
    patient = get_object_or_404(Utilisateur, id=user_id)
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.patient = patient
            consultation.save()
            return redirect('list_consultation', user_id=patient.id)
    else:
        form = ConsultationForm()
    return render(request, 'consultations/form.html', {'form': form, 'patient': patient})

@login_required
def update_consultation(request, id):
    consultation = get_object_or_404(Consultation, id=id)
    if request.method == 'POST':
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            form.save()
            return redirect('list_consultation', user_id=consultation.patient.id)
    else:
        form = ConsultationForm(instance=consultation)
    return render(request, 'consultations/form.html', {'form': form, 'patient': consultation.patient})