# Engage-Santé

Engage-Santé est une application web destinée à la gestion de patientèle et l'historique des consultations médicales. Ce projet est conçu pour aider les médecins à gérer efficacement les informations de leurs patients et leurs consultations, tout en offrant aux patients un accès sécurisé à leurs propres données.

## Installation

> Nécessite Docker et Docker Compose

Créer un fichier `.env` dont voici un exemple pour usage local :

```env
# WEB CONTAINER
PORT=8000

# POSTGRES DATABASE CONTAINER
POSTGRES_VERSION=latest
POSTGRES_DB=engage_sante_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_PORT=5432
```

```bash
cd scripts
sh init.sh
```

## Démarrage

```bash
cd scripts
# Optionel
sh superuser.sh # Pour créer un super user et accéder à localhost:PORT/admin/
cd commands
sh patients.sh N # Avec N le nombre de patients aléatoires à créer
sh medecin.sh # Pour créer un médecin qui pourra visualiser la liste des patients et accéder aux consultations
```

Puis aller sur <http://localhost:8000/connexion/>

## URLS

Voici la liste des urls utiles

```text
Patients :
patients/ [name='list_patients']
patients/<int:user_id>/ [name='info_utilisateur']
modifier/<int:user_id>/ [name='update_utilisateur']
supprimer/<int:user_id>/ [name='delete_utilisateur']

Authentification :
connexion/ [name='login']
deconnexion/ [name='logout']
enregistrer/patient/ [name='register_patient']
enregistrer/medecin/ [name='register_medecin']

Consultations :
patients/<int:patient_id>/consultations/ [name='list_consultation']
patients/<int:patient_id>/consultations/creer/ [name='create_consultation']
consultations/<int:id>/modifier/ [name='update_consultation']
consultations/<int:id>/supprimer/ [name='delete_consultation']
```
