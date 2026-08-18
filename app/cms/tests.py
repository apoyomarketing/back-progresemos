from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from app.usuarios.models import Usuario
from .models import (
    CategoriaPublicacion,
    Publicacion,
    Multimedia,
    Carrusel,
    Documento,
    ConfiguracionSitio,
)


class CMSAPITests(APITestCase):

    def setUp(self):
        self.admin = Usuario.objects.create_user(
            email="admin@test.com",
            nombre="Admin",
            password="123456789",
            is_staff=True,
        )

        self.categoria = CategoriaPublicacion.objects.create(
            nombre="Noticias"
        )

    def autenticar_admin(self):
        self.client.force_authenticate(user=self.admin)

    def test_categoria_genera_slug(self):
        self.assertEqual(
            self.categoria.slug,
            "noticias"
        )

    def test_categorias_son_publicas(self):
        response = self.client.get(
            reverse("categorias-publicacion-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

    def test_admin_puede_crear_categoria(self):
        self.autenticar_admin()

        response = self.client.post(
            reverse("categorias-publicacion-list"),
            {
                "nombre": "Eventos"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["slug"],
            "eventos"
        )

    def test_publico_no_ve_borradores(self):
        Publicacion.objects.create(
            categoria=self.categoria,
            usuario=self.admin,
            titulo="Noticia borrador",
            contenido="Contenido",
            estado="borrador",
        )

        response = self.client.get(
            reverse("publicaciones-list")
        )

        self.assertEqual(
            response.data["count"],
            0
        )

    def test_publico_si_ve_publicadas(self):
        Publicacion.objects.create(
            categoria=self.categoria,
            usuario=self.admin,
            titulo="Noticia publicada",
            contenido="Contenido",
            estado="publicado",
        )

        response = self.client.get(
            reverse("publicaciones-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

    def test_crear_publicacion_asigna_usuario(self):
        self.autenticar_admin()

        response = self.client.post(
            reverse("publicaciones-list"),
            {
                "categoria": self.categoria.pk,
                "titulo": "Nueva noticia",
                "resumen": "Resumen",
                "contenido": "Contenido de prueba",
                "estado": "borrador",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["usuario"],
            self.admin.pk
        )

        self.assertEqual(
            response.data["slug"],
            "nueva-noticia"
        )

    def test_publicar_asigna_fecha_publicacion(self):
        publicacion = Publicacion.objects.create(
            categoria=self.categoria,
            usuario=self.admin,
            titulo="Noticia fecha",
            contenido="Contenido",
            estado="borrador",
        )

        self.autenticar_admin()

        response = self.client.patch(
            reverse(
                "publicaciones-detail",
                args=[publicacion.slug]
            ),
            {
                "estado": "publicado"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIsNotNone(
            response.data["fecha_publicacion"]
        )

    def test_multimedia_inactiva_no_es_publica(self):
        Multimedia.objects.create(
            usuario=self.admin,
            titulo="Video oculto",
            tipo="video",
            url_externa="https://example.com/video",
            activo=False,
        )

        response = self.client.get(
            reverse("multimedia-list")
        )

        self.assertEqual(
            response.data["count"],
            0
        )

    def test_multimedia_inactiva_visible_para_admin(self):
        Multimedia.objects.create(
            usuario=self.admin,
            titulo="Video oculto",
            tipo="video",
            url_externa="https://example.com/video",
            activo=False,
        )

        self.autenticar_admin()

        response = self.client.get(
            reverse("multimedia-list")
        )

        self.assertEqual(
            response.data["count"],
            1
        )

    def test_carrusel_inactivo_no_es_publico(self):
        imagen = SimpleUploadedFile(
            "banner.jpg",
            b"contenido-imagen-prueba",
            content_type="image/jpeg",
        )

        Carrusel.objects.create(
            titulo="Banner",
            imagen=imagen,
            activo=False,
        )

        response = self.client.get(
            reverse("carruseles-list")
        )

        self.assertEqual(
            response.data["count"],
            0
        )

    def test_documento_activo_es_publico(self):
        archivo = SimpleUploadedFile(
            "documento.txt",
            b"Documento de prueba",
            content_type="text/plain",
        )

        Documento.objects.create(
            usuario=self.admin,
            titulo="Documento",
            archivo=archivo,
            tipo_archivo="txt",
            activo=True,
        )

        response = self.client.get(
            reverse("documentos-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

    def test_configuracion_solo_permite_un_registro(self):
        ConfiguracionSitio.objects.create(
            nombre_partido="Progresemos"
        )

        self.autenticar_admin()

        response = self.client.post(
            reverse("configuracion-sitio-list"),
            {
                "nombre_partido": "Otro partido"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            ConfiguracionSitio.objects.count(),
            1
        )