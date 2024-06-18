from django.core.management.base import BaseCommand
from faker import Faker
from patients.models import Utilisateur as Medecin
from patients.models import generate_unique_username
import getpass

fake = Faker('fr_FR')

class Command(BaseCommand):
    help = "Créé un médecin"

    def handle(self, *args, **options):
        last_name = input("Entrer le nom de famille : ")
        first_name = input("Entrer le prénom : ")
        password = None
        password_confirm = None
        while not password or not password_confirm or (password != password_confirm):
            if password and password_confirm:
                self.stdout.write(
                    self.style.ERROR('Les mots de passe sont différents')
                )
            password = getpass.getpass(prompt="Mot de passe : ")
            password_confirm = getpass.getpass(prompt="Confirmer le mot de passe : ")
        username = generate_unique_username(last_name, first_name)
        Medecin.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=fake.email(),
            rue=fake.street_address(),
            cp=fake.postcode(),
            ville=fake.city(),
            is_medecin=True,
            is_staff=True,
        )

        self.stdout.write(
            self.style.SUCCESS('Le medecin a bien été créé, identifiant unique : "%s".' % username)
        )