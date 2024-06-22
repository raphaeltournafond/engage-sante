# Spécifications Technique

## Objectif

Développement d’une application pour gérer une patientèle ainsi que l’historique des
consultations.

## Technologies

✅ Framework Django avec template

Le projet contient deux applications, la première `patients` contient tout ce qui est lié à la gestion des utilisateurs et l’application consultations qui contient le modèle `consultations` et la CRUD associée.

✅ Docker pour la DB et l’environnement développement

La mise en place de Docker est faite en plusieurs étapes :

1. Création des fichiers [`Dockerfile`](../Dockerfile) et [`requirements.txt`](../requirements.txt)
2. Création du fichier [`docker-compose.yml`](../docker-compose.yml)
3. Setup des variables d'environement dans un fichier `.env` dont voici un exemple :

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

✅ PostgreSQL

Une fois le container Postgres créé il ne reste plus qu'à la connecter à l'application dans les [`settings.py`](../engage_sante/settings.py)

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'engage_sante_db'),
        'USER': os.getenv('POSTGRES_USER', 'admin'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
        'HOST': 'db',
        'PORT': os.getenv('POSTGRES_PORT', ''), # If left empty default port is 5432
    }
}
```

✅ Tailwind + DaisyUI

Mise en place de Tailwind CSS en utilisant `npm install tailwindcss` et `npx init` puis configuration du fichier [`tailwind.config.js`](../tailwind.config.js) pour intégrer DaisyUI (utilisé pour les composants classique et les modales).

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./patients/**/*.{html,js}",
    "./templates/**/*.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: ["pastel", "forest"],
    darkTheme: "forest",
  },
}
```

Setup des composants de base de tailwind dans [`static/tailwind/tailwind-input.css`](../static/tailwind/tailwind-input.css).

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Script `node.js` pour la mise à jour du fichier [`static/css/engage-ui.css`](../static/css/engage-ui.css) automatique en dévelopement dans [`package.json`](../package.json).

```json
{
  "scripts": {
    "dev": "tailwindcss -i static/tailwind/tailwind-input.css -o static/css/engage-ui.css --watch"
  },
  "devDependencies": {
    "daisyui": "^4.12.2",
    "tailwindcss": "^3.4.4"
  }
}
```

Enfin ajout du css généré dans [`templates/shared/base.html`](../templates/shared/base.html)

Ce fichier contient les blocs de contenu réutilisés dans les autres pages ainsi que le header et footer du site.

```html
{% load static %}
<!DOCTYPE html>
<html>
  <head>
    <title>
      {% block title %}
        Engage Santé
      {% endblock %}
    </title>
    <link rel="stylesheet" href="{% static 'css/engage-ui.css' %}" type="text/css" />
    ...
```

✅ Intégrer une utilisation pertinente de HTMX

J'ai décidé d'utiliser HTMX pour la suppression des consultations dans la page [`patients/update.html`](../patients/templates/patients/update.html)

```html
<script src="https://unpkg.com/htmx.org@2.0.0" integrity="sha384-wS5l5IKJBvK6sPTKa2WZ1js3d947pvWXbPJ1OmWfEuxLgeHcEbjUUA5i9V5ZkpCw" crossorigin="anonymous"></script>
...
<button
    class="btn btn-error"
    hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}' 
    hx-delete="{% url 'delete_consultation' consultation.id %}"
    hx-on:delete-consultation="this.closest('tr').remove()"
>
    Supprimer
</button>
```

Ici j'importe le **CDN** HTMX puis je créé un bouton de suppression qui enverra la commande de suppression en prenant soin d'intégrer le token CSRF de la session courante. Une fois l'opération de suppression terminée un signal appelé `delete-consultation` est envoyé et la ligne correspondante est effacée du tableau.

Voici la `view` de suppression de consultation dans [`consultations/views.py`](../consultations/views.py)

```py
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
```

## Consignes

### Patients

* 2 types d’utilisateurs différents
  * Médecins (admin)
  * Patients (ne peut consulter que les données le concernant)

* Affichage de la liste des patients

* Ajouter/modifier/supprimer un patient

* Données pour un patient:
  * Identifiant
  * Nom
  * Prénom
  * Email (n’est pas l’identifiant)
  * Adresse complète
  * Le code postal et la ville doivent être récupérés depuis l’api officiel du gouvernement via un selecttype select2

Voici le modèle utilisateur custom que j'ai créé. Voir [`patients/models.py`](../patients/models.py) pour plus de détails notemment la génération de **usernames uniques**.

```py
class Utilisateur(AbstractUser):
    # Champs relatifs a l'adresse
    rue = models.CharField(max_length=100)
    cp = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)
    # Utilisé pour savoir si c'est un medecin
    is_medecin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and not self.username:
            # Génération d'un username unique
            self.username = generate_unique_username(self.last_name, self.first_name)
            if self.is_medecin:
                self.is_staff = True
        super(Utilisateur, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.username
```

Toute les actions CRUD des patients se situent dans [`patients/views.py`](../patients/views.py)

* Créer une commande Django qui va créer 5000 patients en base

La commande `populate [nombre]` permet de créer des patients. Environ 18 minutes pour en créer 5000.

Elle se situe dans [`patients/management/commands/populate.py`](../patients/management/commands/populate.py)

Vous pouvez l'appeler dans [`scripts/commands/patients.sh`](../scripts/commands/patients.sh)
  
### Consultations

* Affichage de la liste des consultations d’un patient

* Ajouter/modifier/supprimer une consultation

* Données pour une consultation :
  * Patient
  * Nom
  * Description
  * Date
  * Type => Visite, Suivi, Opération

Voici le modèle consultation j'ai créé : [`consultations/models.py`](../consultations/models.py).

```py
from django.db import models
from patients.models import Utilisateur

class Consultation(models.Model):
    TYPE_CHOICES = [
        ('Visite', 'Visite'),
        ('Suivi', 'Suivi'),
        ('Operation', 'Opération'),
    ]

    patient = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='consultations')
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.nom} - {self.patient.first_name} {self.patient.last_name}"
```

Toute les actions CRUD des consultations se situent dans [`consultations/views.py`](../consultations/views.py)

### Général

* Modale de confirmation pour la suppression

J'ai utilisé DaisyUI pour la création des modales : [https://daisyui.com/components/modal/](https://daisyui.com/components/modal/). Voici mon implémentation pour la suppression d'un utilisateur dans [`patients/update.html`](../patients/templates/patients/update.html)

```html
{% if user.is_staff %}
    <button class="btn btn-error" onclick="user_delete_modal.showModal()">Supprimer</button>
    <dialog id="user_delete_modal" class="modal modal-bottom sm:modal-middle">
        <div class="modal-box">
            <h3 class="font-bold text-lg">Supprimer un utilisateur</h3>
            <p class="py-4 font-normal text-base">Êtes-vous sûr de vouloir supprimer l'utilisateur {{ utilisateur.last_name }} {{ utilisateur.first_name }} ?</p>
            <div class="modal-action">
                <form method="dialog">
                    <button class="btn btn-outline">Annuler</button>
                </form>
                <form method="post" action="{% url 'delete_utilisateur' utilisateur.id %}">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-error">Supprimer</button>
                </form>
            </div>
        </div>
    </dialog>
{% endif %}
```
  
* Fichier docker-compose.yml pour le déploiement.

Voici le fichier créé :

```yml
name: engage_sante
services:
  # Base de donnée Postgres
  db:
    image: postgres:${POSTGRES_VERSION}
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "${POSTGRES_PORT}:5432"

  # Container d'application Django
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:${PORT}
    ports:
      - "${PORT}:${PORT}"
    volumes:
      - .:/code
    depends_on:
      - db

volumes:
  postgres_data:
```
  
* (Option) Mettre en ligne l’application

Je n'ai pas mis en ligne l'application mais j'ai mis en place des tests unitaires de base pour l'utilisateur et une CI

Ceci implique la création d'un fichier [`docker-compose.test.yml`](../docker-compose.test.yml) et [`settings_test.py`](../engage_sante/settings_test.py) spécifique pour les tests.

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_password',
        'HOST': 'test-db',
        'PORT': 5432, # If left empty default port is 5432
    }
}
```

Voici la CI en question qui va donc build, déployer et tester l'application lors de chaque push sur les branches `develop` ou `main`.

```yml
name: Build, Deploy and Test

on:
  push:
    branches:
        - develop
        - main

jobs:
  build:
    runs-on: ubuntu-latest

    env:
        PORT: 8000
        POSTGRES_VERSION: latest
        POSTGRES_DB: test_db
        POSTGRES_USER: test_user
        POSTGRES_PASSWORD: test_password
        POSTGRES_PORT: 5432

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build
        run: docker-compose -f docker-compose.test.yml build

      - name: Deploy
        run: docker-compose -f docker-compose.test.yml up -d
    
      - name: Check run 
        run: docker-compose -f docker-compose.test.yml ps

      - name: Run tests
        run: docker-compose -f docker-compose.test.yml exec -T web python manage.py test
```
