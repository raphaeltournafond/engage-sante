from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from patients.models import Utilisateur

@login_required
def list_consultation(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)
    consultations = utilisateur.consultations.all()
    return render(request, 'consultations/list.html', {'consultations': consultations, 'utilisateur': utilisateur})