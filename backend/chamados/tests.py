from rest_framework import status
from rest_framework.test import APITestCase

from chamados.models import Chamado


class ChamadoCreateTests(APITestCase):
    url = "/api/chamados/"

    def test_criacao_valida(self):
        payload = {
            "titulo": "Falha no e-mail",
            "descricao": "A recuperação de senha não chega.",
            "status": Chamado.Status.ABERTO,
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chamado.objects.count(), 1)
        self.assertEqual(response.data["titulo"], payload["titulo"])

    def test_cadastro_sem_titulo(self):
        payload = {
            "descricao": "Chamado sem título",
            "status": Chamado.Status.ABERTO,
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", response.data)
        self.assertIn("obrigatório", str(response.data["titulo"]).lower())
        self.assertEqual(Chamado.objects.count(), 0)

    def test_cadastro_titulo_em_branco(self):
        payload = {
            "titulo": "   ",
            "descricao": "Título vazio",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chamado.objects.count(), 0)


class ChamadoFiltroTests(APITestCase):
    url = "/api/chamados/"

    def setUp(self):
        Chamado.objects.create(titulo="Aberto 1", status=Chamado.Status.ABERTO)
        Chamado.objects.create(
            titulo="Andamento 1", status=Chamado.Status.EM_ANDAMENTO
        )
        Chamado.objects.create(
            titulo="Concluido 1", status=Chamado.Status.CONCLUIDO
        )

    def test_filtro_por_status(self):
        response = self.client.get(self.url, {"status": "ABERTO"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "ABERTO")
        self.assertEqual(response.data[0]["titulo"], "Aberto 1")

    def test_filtro_status_invalido(self):
        response = self.client.get(self.url, {"status": "CANCELADO"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)


class IndicadoresTests(APITestCase):
    url = "/api/indicadores/"

    def test_indicadores(self):
        Chamado.objects.create(titulo="A", status=Chamado.Status.ABERTO)
        Chamado.objects.create(titulo="B", status=Chamado.Status.ABERTO)
        Chamado.objects.create(titulo="C", status=Chamado.Status.EM_ANDAMENTO)
        Chamado.objects.create(titulo="D", status=Chamado.Status.CONCLUIDO)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], 4)
        self.assertEqual(response.data["abertos"], 2)
        self.assertEqual(response.data["em_andamento"], 1)
        self.assertEqual(response.data["concluidos"], 1)
