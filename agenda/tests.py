from datetime import datetime, timezone
import json
# from pytz import timezone
from rest_framework.test import APITestCase

from agenda.models import Agendamento

# Create your tests here.


class TestListagemAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get("/api/agendamentos/")
        self.assertEqual(response.content, b"[]")

    def test_listagem_de_agendamentos_criados(self):
        obj1 = Agendamento.objects.create(
            nome_cliente="testeiro1", data_horario="2020-4-4T00:00:00Z")
        # obj1.save()
        obj2 = Agendamento.objects.create(
            nome_cliente="testeiro2", data_horario="2020-5-5T00:00:00Z")
        # obj2.save()
        response = self.client.get("/api/agendamentos/")
        # data = json.loads(response.content)
        self.assertEqual(json.loads(response.content), [{"id": 1, "nome_cliente": "testeiro1", "data_horario": "2020-04-04T00:00:00Z", "email_cliente": "", "telefone_cliente": ""}, {
                         "id": 2, "nome_cliente": "testeiro2", "data_horario": "2020-05-05T00:00:00Z", "email_cliente": "", "telefone_cliente": ""}])


class TestCriacaoAgendamento(APITestCase):
    def test_cria_agendamento(self):
        agendamento_request_data = {
            "data_horario": "2020-12-06T15:00:00Z",
            "nome_cliente": "testeiro1",
            "email_cliente": "teste@email.com",
            "telefone_cliente": "2345678777"
        }       



        response = self.client.post(
            "/api/agendamentos/", agendamento_request_data, format="json")
        agendamento_criado = Agendamento.objects.get()

        response_get = self.client.get("/api/agendamentos/")

        self.assertEqual(agendamento_criado.data_horario, datetime(2020, 12, 6, 15, 0, tzinfo=timezone.utc))
        self.assertEqual(agendamento_criado.nome_cliente, "testeiro1")
        self.assertEqual(agendamento_criado.email_cliente, "teste@email.com")
        self.assertEqual(agendamento_criado.telefone_cliente, "2345678777")
        self.assertEqual(response.status_code, 201)
        resposta_get = [b'[{"id": 1, "data_horario": "2020-12-06T15:00:00Z", "nome_cliente": "testeiro1", "email_cliente": "teste@email.com", "telefone_cliente": "2345678777"}]']
        self.assertEqual(list(response_get), resposta_get)

    def test_quando_request_e_invalido_retorna_400(self):
        agendamento_request_data = {
            "data_horario": "2020-12-06T15:00:00Z",
            "nome_cliente": "testeiro1",
            "email_cliente": "teste@email.com",
            "telefone_cliente": "2345678"
        }
        response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")
        self.assertEqual(response.status_code, 400)

class TestPatch(APITestCase):
    def test_patch(self):
        agendamento_request_data = {
            "data_horario": "2020-12-06T15:00:00Z",
            "nome_cliente": "testeiro1",
            "email_cliente": "teste@email.com",
            "telefone_cliente": "2345678777"
        }       
        patch_request = {"nome_cliente": "testeiro13"}
        response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")
        agendamento_criado = Agendamento.objects.get()
        response_patch = self.client.patch(f"/api/agendamentos/{agendamento_criado.id}/", patch_request, format="json")
        agendamento_modificado = Agendamento.objects.get()
        
        self.assertEqual(agendamento_criado.data_horario, datetime(2020, 12, 6, 15, 0, tzinfo=timezone.utc))
        self.assertEqual(agendamento_modificado.nome_cliente, "testeiro13")
        self.assertEqual(agendamento_criado.email_cliente, "teste@email.com")
        self.assertEqual(agendamento_criado.telefone_cliente, "2345678777")
        self.assertEqual(response_patch.status_code, 200)
        resposta_get = [b'[{"id": 1, "data_horario": "2020-12-06T15:00:00Z", "nome_cliente": "testeiro13", "email_cliente": "teste@email.com", "telefone_cliente": "2345678777"}]']
        # self.assertEqual(list(response_get), resposta_get)

       