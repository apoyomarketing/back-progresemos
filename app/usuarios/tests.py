from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Rol, Usuario


class UsuariosAPITests(APITestCase):

    def setUp(self):
        self.rol = Rol.objects.create(nombre="Administrador")

        self.admin = Usuario.objects.create_user(
            email="admin@test.com",
            nombre="Admin",
            password="123456789",
            rol=self.rol,
            estado=True,
            is_staff=True,
        )

    def test_password_se_guarda_hasheado(self):
        self.assertTrue(
            self.admin.check_password("123456789")
        )

        self.assertNotEqual(
            self.admin.password,
            "123456789"
        )

    def test_login_jwt(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            {
                "email": "admin@test.com",
                "password": "123456789",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_auth_me_sin_token(self):
        response = self.client.get(
            reverse("me")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_auth_me_con_usuario(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            reverse("me")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["email"],
            "admin@test.com"
        )

        self.assertEqual(
            response.data["nombre"],
            "Admin"
        )

        self.assertEqual(
            response.data["rol"]["nombre"],
            "Administrador"
        )

    def test_roles_requiere_autenticacion(self):
        response = self.client.get(
            reverse("roles-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_admin_puede_listar_roles(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            reverse("roles-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

    def test_admin_puede_crear_rol(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("roles-list"),
            {
                "nombre": "Editor"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Rol.objects.filter(
                nombre="Editor"
            ).exists()
        )

    def test_usuarios_requiere_autenticacion(self):
        response = self.client.get(
            reverse("usuarios-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_admin_puede_listar_usuarios(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            reverse("usuarios-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

    def test_admin_puede_crear_usuario(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("usuarios-list"),
            {
                "rol": self.rol.pk,
                "nombre": "Usuario Prueba",
                "email": "usuario@test.com",
                "password": "987654321",
                "estado": True,
                "is_staff": False,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        usuario = Usuario.objects.get(
            email="usuario@test.com"
        )

        self.assertTrue(
            usuario.check_password("987654321")
        )

        self.assertNotIn(
            "password",
            response.data
        )

    def test_cambiar_password_usa_hash(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            reverse(
                "usuarios-detail",
                args=[self.admin.pk]
            ),
            {
                "password": "987654321"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.admin.refresh_from_db()

        self.assertTrue(
            self.admin.check_password(
                "987654321"
            )
        )

        self.assertFalse(
            self.admin.check_password(
                "123456789"
            )
        )