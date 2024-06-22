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

Puis initialiser le container Docker avec la commande suivante :

```bash
cd scripts
sh init.sh
```

## Démarrage

Pour commencer à utiliser l'application il est possible d'utiliser les commandes suivante afin de remplir la base de donnée :

```bash
cd scripts
# Optionel
sh superuser.sh # Pour créer un super user et accéder à localhost:PORT/admin/
cd commands
sh patients.sh N # Avec N le nombre de patients aléatoires à créer
sh medecin.sh # Pour créer un médecin qui pourra visualiser la liste des patients et accéder aux actions staff
```

Puis aller sur <http://localhost:8000/connexion/>

## Documentations

[Document d'usage](DOCS/USAGE.md) de l'application avec screenshots
[Spécification technique](DOCS/SPECIFICATIONS.md) de l'application

## URLS

Voici la liste des urls utiles

### Patients

| Endpoint                                         | Niveau d'accès       | Description                                                    |
|--------------------------------------------------|----------------------|----------------------------------------------------------------|
| `patients/` [name='list_patients']               | Staff only           | Permet de visualiser la liste des patients                     |
| `patients/<int:user_id>/` [name='info_utilisateur'] | Staff ou Utilisateur | Permet de visualiser les informations et consultations d'un utilisateur |
| `modifier/<int:user_id>/` [name='update_utilisateur'] | Staff ou Utilisateur | Permet de modifier les informations et consultations d'un utilisateur |
| `supprimer/<int:user_id>/` [name='delete_utilisateur'] | Staff only           | Permet de supprimer un utilisateur                             |

### Authentification

| Endpoint                                        | Niveau d'accès         | Description                                |
|-------------------------------------------------|------------------------|--------------------------------------------|
| `connexion/` [name='login']                     | Pas d'authentification | Permet de se connecter                     |
| `deconnexion/` [name='logout']                  | Utilisateur            | Permet de déconnecter l'utilisateur courant |
| `enregistrement/patient/` [name='register_patient'] | Pas d'authentification | Permet de créer un compte                  |
| `enregistrement/medecin/` [name='register_medecin'] | Staff only             | Permet d'ajouter un médecin                |

### Consultations

| Endpoint                                               | Niveau d'accès       | Description                                         |
|--------------------------------------------------------|----------------------|-----------------------------------------------------|
| `patients/<int:patient_id>/consultations/creer/` [name='create_consultation'] | Staff only           | Permet de créer une nouvelle consultation pour un patient |
| `consultations/<int:id>/modifier/` [name='update_consultation'] | Staff only           | Permet de modifier une consultation                 |
| `consultations/<int:id>/supprimer/` [name='delete_consultation'] | Staff only           | Permet de supprimer une consultation                |
