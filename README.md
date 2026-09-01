# Sistema de Chamados — Nexa Solutions

API REST de chamados internos com interface HTML, PostgreSQL em container e execução reproduzível via Docker Compose.

## Tecnologias

- Python 3.12
- Django e Django REST Framework
- PostgreSQL 16
- Docker e Docker Compose
- GitHub Actions

## Estrutura

```text
backend/    API Django
frontend/   Interface HTML
docs/       Demandas da empresa
```

## Configuração

Copie o arquivo de exemplo e ajuste os valores locais:

```powershell
Copy-Item .env.example .env
```

O arquivo `.env` não é versionado. Use apenas valores de exemplo em `.env.example`.

## Execução com Docker

```powershell
docker compose up --build
```

A aplicação fica em `http://localhost:8000/`.

A API fica em `http://localhost:8000/api/chamados/`.

O Compose sobe o PostgreSQL, espera o banco ficar saudável, aplica as migrations e inicia o backend.

## Testes

Com o ambiente Docker em execução:

```powershell
docker compose exec api python manage.py test
```

Fora do Docker, com as dependências instaladas:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py test
```

Os testes cobrem criação válida, cadastro sem título, filtro por status e indicadores.

O GitHub Actions executa os mesmos testes em todo push e pull request para `main`.

## Endpoints

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/api/chamados/` | Lista chamados |
| GET | `/api/chamados/?status=ABERTO` | Filtra por status (`ABERTO`, `EM_ANDAMENTO`, `CONCLUIDO`) |
| POST | `/api/chamados/` | Cria chamado. `titulo` é obrigatório |
| GET | `/api/chamados/<id>/` | Detalha um chamado |
| PATCH | `/api/chamados/<id>/` | Atualiza um chamado |
| GET | `/api/indicadores/` | Totais geral, abertos, em andamento e concluídos |

Exemplo de criação:

```json
{
  "titulo": "Falha no login",
  "descricao": "Usuário não consegue autenticar.",
  "status": "ABERTO"
}
```

Cadastro sem título retorna HTTP 400 com a mensagem de que o título é obrigatório.

Status inválido no filtro retorna HTTP 400.

Exemplo de indicadores:

```json
{
  "total": 4,
  "abertos": 2,
  "em_andamento": 1,
  "concluidos": 1
}
```

## Decisões técnicas

- Segredos e credenciais vêm de variáveis de ambiente.
- PostgreSQL persiste dados em volume nomeado.
- O backend só sobe depois do healthcheck do banco.
- Testes usam SQLite em memória para executar sem o container.
- A interface HTML é servida em `/` pelo Django para evitar CORS em desenvolvimento.

## Evidências

- Issues INC-01 a INC-07 no GitHub.
- Branches e Pull Requests no fork `lul-cas/nexa-solutions`.
- Validação local com `docker compose up --build`.
