import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from cms.models import (
    CategoriaPublicacion,
    Publicacion,
    Multimedia,
    Carrusel,
    Documento,
    ConfiguracionSitio,
)

User = get_user_model()

class CmsApiTests(APITestCase):
    def setUp(self):
        # Create a regular user for authentication
        self.user = User.objects.create_user(email='test@example.com', nombre='Test User', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create sample data
        self.categoria = CategoriaPublicacion.objects.create(nombre='Noticias')
        self.publicacion = Publicacion.objects.create(
            titulo='Primer Post',
            contenido='Contenido del post',
            categoria=self.categoria,
            estado='publicado',
        )
        self.multimedia = Multimedia.objects.create(
            tipo='imagen',
            archivo='multimedia/img.jpg',
            activo=True,
            publicacion=self.publicacion,
        )
        self.carrusel = Carrusel.objects.create(nombre='Home', activo=True, orden=1)
        self.carrusel.multimedia.add(self.multimedia)
        self.documento = Documento.objects.create(
            archivo='documentos/doc.pdf',
            activo=True,
            publicacion=self.publicacion,
        )
        ConfiguracionSitio.objects.create(clave='site_name', valor='Demo')

    def test_categoria_public_read_public(self):
        url = reverse('categorias-publicacion-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_categoria_public_create_authenticated(self):
        url = reverse('categorias-publicacion-list')
        data = {'nombre': 'Eventos', 'descripcion': 'Eventos del mes'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_publicacion_list_public_only_published(self):
        url = reverse('publicaciones-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only published should appear
        self.assertTrue(all(item['estado'] == 'publicado' for item in response.data))

    def test_publicacion_create_authenticated(self):
        url = reverse('publicaciones-list')
        data = {
            'titulo': 'Nuevo Post',
            'contenido': 'Texto',
            'categoria': self.categoria.id,
            'estado': 'borrador',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_publicacion_filter_by_estado(self):
        url = reverse('publicaciones-list') + '?estado=borrador'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item['estado'] == 'borrador' for item in response.data))

    def test_publicacion_filter_by_categoria(self):
        url = reverse('publicaciones-list') + f'?categoria={self.categoria.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item['categoria'] == self.categoria.id for item in response.data))

    def test_publicacion_retrieve_by_slug(self):
        url = reverse('publicaciones-detail', args=[self.publicacion.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.publicacion.slug)

    def test_multimedia_filter_activo_and_tipo(self):
        url = reverse('multimedia-list') + '?activo=true&tipo=imagen'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            self.assertTrue(item['activo'])
            self.assertEqual(item['tipo'], 'imagen')

    def test_carrusel_filter_activo_and_order(self):
        url = reverse('carruseles-list') + '?activo=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure ordering by 'orden'
        orders = [item['orden'] for item in response.data]
        self.assertEqual(orders, sorted(orders))

    def test_documento_filter_activo(self):
        url = reverse('documentos-list') + '?activo=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item['activo'] for item in response.data))

    def test_configuracion_sitio_singleton(self):
        # Attempt to create another config should update existing
        url = reverse('configuracion-sitio-list')
        data = {'clave': 'site_name', 'valor': 'NuevoNombre'}
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        self.assertEqual(ConfiguracionSitio.objects.count(), 1)
        self.assertEqual(ConfiguracionSitio.objects.first().valor, 'NuevoNombre')

