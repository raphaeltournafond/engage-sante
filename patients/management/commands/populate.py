from django.core.management.base import BaseCommand
from faker import Faker
from tqdm import trange
from patients.models import Utilisateur as Patient
from patients.models import generate_unique_username

fake = Faker('fr_FR')

class Command(BaseCommand):
    help = "Ajoute des patients aléatoires dans la base de donnée"

    def add_arguments(self, parser):
        parser.add_argument("nombre", nargs="?", type=int)

    def handle(self, *args, **options):
        nombre = options["nombre"] if options["nombre"] else 1
        patients = []
        cache = []
        batch_size = 10
        for n in trange(nombre, desc="Création des patients"):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = generate_unique_username(last_name, first_name, cache)
            cache.append(username)
            patient = Patient(
                username=username,
                first_name = first_name,
                last_name = last_name,
                email=fake.email(),
                rue=fake.street_address(),
                cp=fake.postcode(),
                ville=fake.city(),
                is_medecin=False
            )
            patient.set_password(fake.password())
            patients.append(patient)

            if n % batch_size == 0:
                Patient.objects.bulk_create(patients, batch_size=batch_size)
                patients.clear()

        Patient.objects.bulk_create(patients, batch_size=batch_size)

        self.stdout.write(
            self.style.SUCCESS('Les "%s" patients ont bien été ajoutés.' % nombre)
        )