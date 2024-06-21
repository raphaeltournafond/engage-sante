from django.test import TestCase
from .models import Utilisateur, generate_unique_username

class UtilisateurTestCase(TestCase):

    def setUp(self):
        self.utilisateur1 = Utilisateur.objects.create(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            rue="123, Main Street",
            cp="12345",
            ville="City",
            is_medecin=False
        )
        self.utilisateur2 = Utilisateur.objects.create(
            username="janedoe",
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            rue="456, Elm Street",
            cp="67890",
            ville="Town",
            is_medecin=True
        )

    def test_generate_unique_username(self):
        unique_username = generate_unique_username("Smith", "Alice")
        self.assertEqual(unique_username, "smithal")

        existing_username = generate_unique_username("Doe", "John")
        self.assertNotEqual(existing_username, "johndoe")

        cache = ["johndoe", "smithal"]
        unique_username_with_cache = generate_unique_username("Smith", "Alice", cache)
        self.assertNotIn(unique_username_with_cache, cache)

    def test_save_utilisateur(self):
        new_utilisateur = Utilisateur(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            rue="789, Oak Avenue",
            cp="54321",
            ville="Village",
            is_medecin=False
        )
        new_utilisateur.save()
        self.assertIsNotNone(new_utilisateur.username)
        self.assertNotEqual(new_utilisateur.username, "janesm")

        new_doctor = Utilisateur(
            first_name="James",
            last_name="Brown",
            email="james.brown@example.com",
            rue="456, Pine Street",
            cp="98765",
            ville="City",
            is_medecin=True
        )
        new_doctor.save()
        self.assertTrue(new_doctor.is_staff)
