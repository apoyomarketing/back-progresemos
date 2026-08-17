from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Departamento, Provincia, Distrito


class UbicacionesAPITests(APITestCase):

    def setUp(self):
        self.puno = Departamento.objects.create(
            nombre="Puno"
        )

        self.cusco = Departamento.objects.create(
            nombre="Cusco"
        )

        self.provincia_puno = Provincia.objects.create(
            departamento=self.puno,
            nombre="Puno"
        )

        self.provincia_sandia = Provincia.objects.create(
            departamento=self.puno,
            nombre="Sandia"
        )

        self.provincia_cusco = Provincia.objects.create(
            departamento=self.cusco,
            nombre="Cusco"
        )

        self.distrito_puno = Distrito.objects.create(
            provincia=self.provincia_puno,
            nombre="Puno"
        )

        self.distrito_acora = Distrito.objects.create(
            provincia=self.provincia_puno,
            nombre="Acora"
        )

        self.distrito_sandia = Distrito.objects.create(
            provincia=self.provincia_sandia,
            nombre="Sandia"
        )

    def test_departamentos_son_publicos(self):
        response = self.client.get(
            reverse("departamentos-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            2
        )

    def test_provincias_son_publicas(self):
        response = self.client.get(
            reverse("provincias-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            3
        )

    def test_filtrar_provincias_por_departamento(self):
        response = self.client.get(
            reverse("provincias-list"),
            {
                "departamento": self.puno.pk
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            2
        )

    def test_distritos_son_publicos(self):
        response = self.client.get(
            reverse("distritos-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            3
        )

    def test_filtrar_distritos_por_provincia(self):
        response = self.client.get(
            reverse("distritos-list"),
            {
                "provincia": self.provincia_puno.pk
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            2
        )

        nombres = [
            item["nombre"]
            for item in response.data["results"]
        ]

        self.assertIn("Puno", nombres)
        self.assertIn("Acora", nombres)