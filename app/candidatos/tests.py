from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from app.usuarios.models import Usuario
from .models import Cargo, Candidato


class CandidatosAPITests(APITestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email="admin@test.com",
            nombre="Admin",
            password="123456789",
            is_staff=True,
        )

        self.cargo = Cargo.objects.create(
            nombre="Presidente"
        )

        self.client.force_authenticate(
            user=self.usuario
        )

    def test_listar_cargos(self):
        response = self.client.get(
            reverse("cargos-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

    def test_crear_cargo(self):
        response = self.client.post(
            reverse("cargos-list"),
            {
                "nombre": "Vicepresidente"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Cargo.objects.filter(
                nombre="Vicepresidente"
            ).exists()
        )

    def test_candidatos_requiere_autenticacion(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(
            reverse("candidatos-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_crear_candidato(self):
        response = self.client.post(
            reverse("candidatos-list"),
            {
                "id_cargo": self.cargo.pk,
                "nombres": "Juan Carlos",
                "apellido_paterno": "Perez",
                "apellido_materno": "Quispe",
                "descripcion": "Candidato de prueba",
                "orden": 1,
                "activo": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["nombres"],
            "Juan Carlos"
        )

        self.assertEqual(
            response.data["cargo"]["nombre"],
            "Presidente"
        )

    def test_listar_candidatos(self):
        Candidato.objects.create(
            cargo=self.cargo,
            nombres="Juan",
            apellido_paterno="Perez",
            apellido_materno="Quispe",
            descripcion="Prueba",
            orden=1,
            activo=True,
        )

        response = self.client.get(
            reverse("candidatos-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

    def test_filtrar_candidatos_por_activo(self):
        Candidato.objects.create(
            cargo=self.cargo,
            nombres="Activo",
            apellido_paterno="Perez",
            activo=True,
        )

        Candidato.objects.create(
            cargo=self.cargo,
            nombres="Inactivo",
            apellido_paterno="Quispe",
            activo=False,
        )

        response = self.client.get(
            reverse("candidatos-list"),
            {
                "activo": "true"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

        self.assertEqual(
            response.data["results"][0]["nombres"],
            "Activo"
        )

    def test_filtrar_candidatos_por_cargo(self):
        otro_cargo = Cargo.objects.create(
            nombre="Alcalde"
        )

        Candidato.objects.create(
            cargo=self.cargo,
            nombres="Candidato Uno",
            apellido_paterno="Perez",
        )

        Candidato.objects.create(
            cargo=otro_cargo,
            nombres="Candidato Dos",
            apellido_paterno="Quispe",
        )

        response = self.client.get(
            reverse("candidatos-list"),
            {
                "cargo": self.cargo.pk
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

        self.assertEqual(
            response.data["results"][0]["nombres"],
            "Candidato Uno"
        )