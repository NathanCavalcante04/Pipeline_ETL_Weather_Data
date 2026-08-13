# Pipeline ETL - Dados de Clima (OpenWeatherMap)

Pipeline de dados end-to-end que extrai dados climáticos em tempo real da API do OpenWeatherMap, transforma e estrutura os dados com Pandas, e carrega em um banco PostgreSQL — tudo orquestrado pelo Apache Airflow e containerizado com Docker.

## Arquitetura

```
OpenWeatherMap API
        │
        ▼
   [ EXTRACT ]  →  salva JSON bruto em disco
        │
        ▼
  [ TRANSFORM ]  →  normaliza, limpa e tipa os dados (Pandas) → Parquet
        │
        ▼
    [ LOAD ]  →  carrega os dados no PostgreSQL
        │
        ▼
   PostgreSQL (tabela sp_weather)
```

Todo o fluxo é orquestrado por uma DAG do Airflow (`weather_dags.py`), executada de hora em hora, com retries automáticos em caso de falha.

## Stack

- **Python** — lógica de extração, transformação e carga
- **Apache Airflow** (TaskFlow API) — orquestração e agendamento
- **Pandas** — transformação e normalização dos dados
- **PostgreSQL** + **SQLAlchemy** — armazenamento
- **Docker / Docker Compose** — containerização de todo o ambiente
- **uv** — gerenciamento de dependências

## Estrutura do projeto

```
├── dags/
│   └── weather_dags.py          # DAG do Airflow (extract → transform → load)
├── src/projetoengenharia/
│   ├── extract_data.py          # Extração via API OpenWeatherMap
│   ├── transform_data.py        # Limpeza, normalização e tipagem
│   └── load_data.py             # Carga no PostgreSQL
├── notebooks/                   # Exploração e testes pontuais
├── docker-compose.yaml
├── pyproject.toml
└── config/.env                  # Variáveis de ambiente (não versionado)
```

## Como rodar

**Pré-requisitos:** Docker e Docker Compose instalados.

1. Clone o repositório:
   ```bash
   git clone https://github.com/NathanCavalcante04/Pipeline_ETL_Weather_Data.git
   cd Pipeline_ETL_Weather_Data
   ```

2. Crie o arquivo `config/.env` com suas credenciais:
   ```env
   API_KEY=sua_chave_openweathermap
   user=airflow
   password=sua_senha
   database=weather_db
   host=postgres
   ```

3. Suba o ambiente:
   ```bash
   docker-compose up -d
   ```

4. Acesse a UI do Airflow em `http://localhost:8080`, ative a DAG `projeto_weather_pipeline` e acompanhe a execução.

5. Os dados carregados ficam disponíveis na tabela `sp_weather` do PostgreSQL.

## Pipeline (DAG)

A DAG `projeto_weather_pipeline` roda a cada hora (`0 * * * *`) e é composta por três tasks sequenciais:

1. **extract** — consulta a API do OpenWeatherMap para a cidade de São Paulo e salva o JSON bruto em disco.
2. **transform** — normaliza colunas aninhadas (ex: `main.temp`, `weather[0].description`), remove colunas irrelevantes, renomeia para nomes legíveis e converte timestamps para o fuso `America/Sao_Paulo`. Salva o resultado em Parquet.
3. **load** — lê o Parquet e insere os dados no PostgreSQL via SQLAlchemy.

Os dados trafegam entre as tasks via arquivo em disco (JSON → Parquet), não via XCom do Airflow — decisão deliberada, já que XCom não é adequado para volumes de dados tabulares.

## Melhorias futuras

- [ ] Parametrizar cidade e nome da tabela via Airflow Variables
- [ ] Adicionar testes unitários para as funções de transformação
- [ ] Dashboard de visualização (Metabase / Looker Studio)
- [ ] Validação de schema/qualidade de dados (ex: Great Expectations)
- [ ] CI para rodar lint e testes a cada push

## Autor

Nathan Cavalcante da Silva
[LinkedIn](https://linkedin.com/in/nathancavalcante04) · [GitHub](https://github.com/NathanCavalcante04)
