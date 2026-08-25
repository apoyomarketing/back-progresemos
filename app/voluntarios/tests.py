"""
Corre con:  python manage.py test app.voluntarios

Decolecta está mockeada: NO consume créditos ni necesita internet.
"""
from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .decolecta import ErrorDni
from .models import ConsultaReniec, LimitadorApi, Voluntario

RESPUESTA_DECOLECTA = {
    "first_name": "ROXANA KARINA",
    "first_last_name": "DELGADO",
    "second_last_name": "HUAMANI",
    "full_name": "DELGADO HUAMANI ROXANA KARINA",
    "document_number": "46027897",
}

PERSONA = {
    "dni": "46027897",
    "nombres": "ROXANA KARINA",
    "apellido_paterno": "DELGADO",
    "apellido_materno": "HUAMANI",
    "nombre_completo": "DELGADO HUAMANI ROXANA KARINA",
}


def cubeta(tokens=3.0, tasa=6.0):
    LimitadorApi.objects.update_or_create(
        clave="decolecta",
        defaults={"tokens": tokens, "capacidad": max(tokens, 3.0), "tasa": tasa},
    )


class FlujoTests(TestCase):
    def setUp(self):
        cubeta()
        self.url_validar = reverse("voluntarios-validar-dni")
        self.url_registrar = reverse("voluntarios-registrar")

    @patch("app.voluntarios.decolecta.consultar_dni", return_value=PERSONA)
    def test_valida_dni_y_devuelve_nombre(self, _):
        r = self.client.post(self.url_validar, {"dni": "46027897"}, "application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["nombre_completo"], PERSONA["nombre_completo"])

    def test_dni_de_7_digitos(self):
        r = self.client.post(self.url_validar, {"dni": "4602789"}, "application/json")
        self.assertEqual(r.status_code, 422)

    @patch("app.voluntarios.decolecta.consultar_dni",
           side_effect=ErrorDni("No encontramos ese DNI.", 404))
    def test_dni_inexistente(self, _):
        r = self.client.post(self.url_validar, {"dni": "99999999"}, "application/json")
        self.assertEqual(r.status_code, 404)
        self.assertIn("detail", r.json())

    @patch("app.voluntarios.decolecta.consultar_dni", return_value=PERSONA)
    def test_registro_crea_voluntario(self, _):
        r = self.client.post(
            self.url_registrar,
            {"dni": "46027897", "celular": "987654321", "acepta_whatsapp": True},
            "application/json",
        )
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.json()["codigo"].startswith("PRG-"))
        v = Voluntario.objects.get(dni="46027897")
        self.assertEqual(v.nombre_completo, PERSONA["nombre_completo"])
        self.assertEqual(v.estado, "preinscrito")

    @patch("app.voluntarios.decolecta.consultar_dni", return_value=PERSONA)
    def test_sin_consentimiento_no_registra(self, _):
        r = self.client.post(
            self.url_registrar,
            {"dni": "46027897", "celular": "987654321", "acepta_whatsapp": False},
            "application/json",
        )
        self.assertEqual(r.status_code, 422)
        self.assertEqual(Voluntario.objects.count(), 0)

    @patch("app.voluntarios.decolecta.consultar_dni", return_value=PERSONA)
    def test_celular_invalido(self, _):
        r = self.client.post(
            self.url_registrar,
            {"dni": "46027897", "celular": "12345678", "acepta_whatsapp": True},
            "application/json",
        )
        self.assertEqual(r.status_code, 422)
        self.assertEqual(Voluntario.objects.count(), 0)

    @patch("app.voluntarios.decolecta.consultar_dni", return_value=PERSONA)
    def test_duplicado_devuelve_409(self, mock):
        datos = {"dni": "46027897", "celular": "987654321", "acepta_whatsapp": True}
        self.client.post(self.url_registrar, datos, "application/json")
        llamadas_antes = mock.call_count
        r = self.client.post(self.url_registrar, datos, "application/json")
        self.assertEqual(r.status_code, 409)
        self.assertEqual(Voluntario.objects.count(), 1)
        # No se gastó otro crédito: el duplicado se detecta antes de consultar.
        self.assertEqual(mock.call_count, llamadas_antes)

    @patch("app.voluntarios.decolecta.consultar_dni", return_value=PERSONA)
    def test_no_confia_en_el_nombre_del_navegador(self, _):
        self.client.post(
            self.url_registrar,
            {
                "dni": "46027897",
                "celular": "987654321",
                "acepta_whatsapp": True,
                "nombre_completo": "NOMBRE FALSO INYECTADO",
            },
            "application/json",
        )
        self.assertEqual(
            Voluntario.objects.get(dni="46027897").nombre_completo,
            PERSONA["nombre_completo"],
        )

    @patch("app.voluntarios.decolecta.consultar_dni", return_value=PERSONA)
    def test_guarda_ip_del_proxy(self, _):
        self.client.post(
            self.url_registrar,
            {"dni": "46027897", "celular": "987654321", "acepta_whatsapp": True},
            "application/json",
            HTTP_X_FORWARDED_FOR="200.10.20.30, 10.0.0.1",
        )
        self.assertEqual(Voluntario.objects.get(dni="46027897").ip, "200.10.20.30")

    @patch("app.voluntarios.decolecta.consultar_dni", return_value=PERSONA)
    def test_endpoint_es_publico(self, _):
        """El proyecto usa IsAuthenticatedOrReadOnly: sin AllowAny esto daría 401."""
        r = self.client.post(self.url_validar, {"dni": "46027897"}, "application/json")
        self.assertNotIn(r.status_code, (401, 403))


class CacheTests(TestCase):
    def setUp(self):
        cubeta()

    @patch("app.voluntarios.decolecta.requests.get")
    def test_segunda_consulta_sale_de_la_tabla(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = RESPUESTA_DECOLECTA
        from .decolecta import consultar_dni

        consultar_dni("46027897")
        consultar_dni("46027897")
        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(ConsultaReniec.objects.count(), 1)

    @patch("app.voluntarios.decolecta.requests.get")
    def test_cache_vencida_vuelve_a_consultar(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = RESPUESTA_DECOLECTA
        from .decolecta import consultar_dni

        consultar_dni("46027897")
        ConsultaReniec.objects.filter(dni="46027897").update(
            updated_at=timezone.now() - timedelta(hours=48)
        )
        consultar_dni("46027897")
        self.assertEqual(mock_get.call_count, 2)


class LimitadorTests(TestCase):
    @patch("app.voluntarios.decolecta.requests.get")
    def test_consume_una_ficha(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = RESPUESTA_DECOLECTA
        cubeta(tokens=3.0, tasa=0.0)
        from .decolecta import consultar_dni

        consultar_dni("46027897")
        self.assertAlmostEqual(
            LimitadorApi.objects.get(clave="decolecta").tokens, 2.0, places=1
        )

    @patch("app.voluntarios.decolecta.time.sleep")
    @patch("app.voluntarios.decolecta.requests.get")
    def test_cubeta_vacia_protege_la_api(self, mock_get, _sleep):
        cubeta(tokens=0.0, tasa=0.0)
        from .decolecta import consultar_dni

        with self.assertRaises(ErrorDni) as ctx:
            consultar_dni("46027897")
        self.assertEqual(ctx.exception.status, 503)
        self.assertEqual(mock_get.call_count, 0)

    @patch("app.voluntarios.decolecta.requests.get")
    def test_la_cubeta_se_rellena_sola(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = RESPUESTA_DECOLECTA
        cubeta(tokens=0.0, tasa=6.0)
        LimitadorApi.objects.filter(clave="decolecta").update(
            actualizado=timezone.now() - timedelta(seconds=1)
        )
        from .decolecta import consultar_dni

        consultar_dni("46027897")
        self.assertEqual(mock_get.call_count, 1)


class CodigoCorrelativoTests(TestCase):
    """El código es PRG- más un correlativo de al menos 4 dígitos."""

    def setUp(self):
        cubeta()

    @patch("app.voluntarios.decolecta.consultar_dni")
    def test_formato_y_orden(self, mock):
        codigos = []
        for i in range(3):
            dni = f"2000{i:04d}"
            mock.return_value = dict(PERSONA, dni=dni)
            r = self.client.post(
                reverse("voluntarios-registrar"),
                {"dni": dni, "celular": "987654321", "acepta_whatsapp": True},
                "application/json",
            )
            self.assertEqual(r.status_code, 201)
            codigos.append(r.json()["codigo"])

        for codigo in codigos:
            self.assertRegex(codigo, r"^PRG-\d{4,}$")

        numeros = [int(c.split("-")[1]) for c in codigos]
        self.assertEqual(numeros, sorted(numeros))
        self.assertEqual(len(set(codigos)), 3)
