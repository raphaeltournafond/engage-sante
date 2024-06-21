from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CustomUtilisateurCreationForm, UtilisateurUpdateForm
from .models import Utilisateur

@login_required
def list_patients(request):
    if request.user.is_staff:
        patients = Utilisateur.objects.filter(is_medecin=False, is_staff=False, is_superuser=False)
        return render(request, 'patients/list.html', {'patients': patients})
    return redirect('not_authorized')

@login_required
def info_utilisateur(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)
    if request.user.is_staff or request.user.id == utilisateur.id:
        return render(request, 'patients/info.html', {'utilisateur': utilisateur})
    return redirect('not_authorized')

@login_required
def update_utilisateur(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)
    if request.user.is_staff or request.user.id == utilisateur.id:
        if request.method == 'POST':
            form = UtilisateurUpdateForm(request.POST, instance=utilisateur)
            if form.is_valid():
                form.save()
                return redirect('info_utilisateur', user_id=utilisateur.id)
        else:
            form = UtilisateurUpdateForm(instance=utilisateur)
        return render(request, 'patients/update.html', {'form': form, 'utilisateur': utilisateur})
    return redirect('not_authorized')

@login_required
def delete_utilisateur(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)
    if request.user.is_staff or request.user.id == utilisateur.id:
        if request.method == 'POST':
            utilisateur.delete()
            return redirect('list_patients')
    return redirect('not_authorized')

class CustomLoginView(LoginView):
    template_name = 'patients/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url(user))

    def get_success_url(self, user):
        return reverse('info_utilisateur', kwargs={'user_id': user.id})

def register_patient(request):
        if request.method == 'POST':
            form = CustomUtilisateurCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_medecin = False
                user.is_staff = False
                user.save()
                login(request, user)
                return redirect('info_utilisateur', user_id=user.id)
            else:
                error_message = None
                if 'password2' in form.errors.as_data():
                    error_message = form.errors.as_data()['password2'][0]

                return render(request, 'patients/register.html', {'form': form, 'error_message': error_message})
        else:
            form = CustomUtilisateurCreationForm()
        return render(request, 'patients/register.html', {'form': form, 'error_message': None})

@login_required
def register_medecin(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CustomUtilisateurCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_medecin = True
                user.is_staff = True
                user.save()
                login(request, user)
                return redirect('list_patients')
            else:
                error_message = None
                if 'password2' in form.errors.as_data():
                    error_message = form.errors.as_data()['password2'][0]

                return render(request, 'patients/register.html', {'form': form, 'error_message': error_message})
        else:
            form = CustomUtilisateurCreationForm()
        return render(request, 'patients/register.html', {'form': form, 'error_message': None})
    return redirect('not_authorized')

def not_authorized(request):
    return render(request, 'patients/not_authorized.html')
