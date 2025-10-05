# Cruise Price Monitor

O projeto **Cruise Price Monitor** tem como objetivo acompanhar e comparar preços de cruzeiros em múltiplas fontes, oferecendo alertas e ferramentas de análise para identificar as melhores ofertas disponíveis.

## Visão Geral

A aplicação é composta pelos seguintes módulos:

- **Scrapers e integrações**: coleta de dados de APIs públicas ou por meio de scraping.
- **Banco de dados PostgreSQL** com versionamento via Alembic.
- **API interna FastAPI** para consulta de cruzeiros, rankings e gerenciamento de alertas.
- **Scheduler diário** que atualiza preços e registra histórico.
- **Sistema de alertas** com suporte a múltiplos canais (e-mail, Telegram, Slack).
- **Monitoramento** com logs estruturados e métricas para observabilidade.

## Requisitos

- Python 3.12+
- PostgreSQL 15+
- [Poetry](https://python-poetry.org/) ou pipenv para gerenciamento de dependências
- Docker / Docker Compose (opcional para desenvolvimento)

## Configuração do Ambiente

1. Clone o repositório e acesse o diretório do projeto:

   ```bash
   git clone <repo-url>
   cd cruise-price-monitor
   ```

2. Copie o arquivo `.env.example` para `.env` e ajuste as variáveis necessárias.

   ```bash
   cp .env.example .env
   ```

3. Instale as dependências com Poetry:

   ```bash
   poetry install
   ```

   Ou com pipenv:

   ```bash
   pipenv install --dev
   ```

4. Execute as migrações do banco de dados:

   ```bash
   poetry run alembic upgrade head
   ```

5. Inicie a aplicação FastAPI em modo de desenvolvimento:

   ```bash
   poetry run uvicorn src.api.main:app --reload
   ```

## Testes

Execute os testes com:

```bash
poetry run pytest
```

## Docker

Para iniciar os serviços com Docker Compose:

```bash
docker compose up --build
```

## Roadmap Futuro

- Dashboard web para visualização dos itinerários e comparativos.
- Integração com APIs de companhias aéreas.
- Módulo de recomendação de roteiros personalizados.
