from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from consultations.forms import ConsultationForm
from patients.models import Utilisateur
from .models import Consultation

@login_required
def list_consultation(request, patient_id):
    patient = get_object_or_404(Utilisateur, id=patient_id)
    if request.user.is_staff or request.user.id == patient.id:
        consultations = patient.consultations.all()
        return render(request, 'consultations/list.html', {'consultations': consultations, 'patient': patient, 'user': request.user})
    return redirect('not_authorized')

@login_required
def create_consultation(request, patient_id):
    if request.user.is_staff:
        patient = get_object_or_404(Utilisateur, id=patient_id)
        if request.method == 'POST':
            form = ConsultationForm(request.POST)
            if form.is_valid():
                consultation = form.save(commit=False)
                consultation.patient = patient
                consultation.save()
                return redirect('update_utilisateur', user_id=consultation.patient.id)
        else:
            form = ConsultationForm()
        return render(request, 'consultations/form.html', {'form': form, 'patient': patient})
    return redirect('not_authorized')

@login_required
def update_consultation(request, id):
    if request.user.is_staff:
        consultation = get_object_or_404(Consultation, id=id)
        if request.method == 'POST':
            form = ConsultationForm(request.POST, instance=consultation)
            if form.is_valid():
                form.save()
                return redirect('update_utilisateur', user_id=consultation.patient.id)
        else:
            form = ConsultationForm(instance=consultation)
        return render(request, 'consultations/form.html', {'form': form, 'patient': consultation.patient})
    return redirect('not_authorized')

@login_required
@require_http_methods(['DELETE'])
def delete_consultation(request, id):
    print('Test')
    if request.user.is_staff:
        consultation = get_object_or_404(Consultation, id=id)
        consultation.delete()
        response = HttpResponse(status=204)
        response['HX-Trigger'] = 'delete-consultation' # Signal HTMX
        return response
    return HttpResponse({'error': 'Vous ne pouvez pas supprimer cette consultation.'}, status=403)