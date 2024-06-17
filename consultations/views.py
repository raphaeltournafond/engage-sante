from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from consultations.forms import ConsultationForm
from patients.models import Utilisateur

@login_required
def list_consultation(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)
    consultations = utilisateur.consultations.all()
    return render(request, 'consultations/list.html', {'consultations': consultations, 'utilisateur': utilisateur})

@login_required
def create_consultation(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.patient = utilisateur
            consultation.save()
            return redirect('list_consultation', user_id=utilisateur.id)
    else:
        form = ConsultationForm()
    return render(request, 'consultations/form.html', {'form': form, 'utilisateur': utilisateur})