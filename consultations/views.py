from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from consultations.forms import ConsultationForm
from patients.models import Utilisateur
from .models import Consultation

@login_required
def list_consultation(request, patient_id):
    patient = get_object_or_404(Utilisateur, id=patient_id)
    consultations = patient.consultations.all()
    return render(request, 'consultations/list.html', {'consultations': consultations, 'patient': patient})

@login_required
def create_consultation(request, patient_id):
    patient = get_object_or_404(Utilisateur, id=patient_id)
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.patient = patient
            consultation.save()
            return redirect('list_consultation', patient_id=patient.id)
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
            return redirect('list_consultation', patient_id=consultation.patient.id)
    else:
        form = ConsultationForm(instance=consultation)
    return render(request, 'consultations/form.html', {'form': form, 'patient': consultation.patient})

@login_required
def delete_consultation(request, id):
    consultation = get_object_or_404(Consultation, id=id)
    if request.method == 'POST':
        consultation.delete()
        return redirect('list_consultation', patient_id=consultation.patient.id)
    return render(request, 'consultations/delete.html', {'consultation': consultation})