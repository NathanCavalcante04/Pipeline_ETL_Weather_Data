# Pipeline ETL de Dados Meteorológicos

Pipeline de dados que coleta informações meteorológicas de São Paulo em tempo real por meio da API OpenWeatherMap, transforma os dados com Pandas e os armazena em PostgreSQL. A execução é orquestrada pelo Apache Airflow e todo o ambiente é executado com Docker Compose.

## Arquitetura

```text
OpenWeatherMap API
        │
        ▼
   Extract (JSON)
        │
        ▼
Transform (Pandas)
        │
        ▼
   Parquet temporário
        │
        ▼
 Load (SQLAlchemy)
        │
        ▼
PostgreSQL — tabela sp_weather
```

A DAG `projeto_weather_pipeline` executa o fluxo `extract → transform → load` a cada hora. Em caso de falha, cada tarefa pode realizar até duas novas tentativas, com intervalo de cinco minutos.

## Tecnologias

- Python
- Apache Airflow com TaskFlow API
- Pandas
- PostgreSQL e SQLAlchemy
- Docker e Docker Compose
- Redis e CeleryExecutor
- Parquet
- uv para gerenciamento das dependências do projeto

## Estrutura do projeto

```text
.
├── dags/
│   └── weather_dags.py
├── src/projetoengenharia/
│   ├── extract_data.py
│   ├── transform_data.py
│   └── load_data.py
├── notebooks/
├── config/
│   └── airflow.cfg
├── data/                         # Arquivos gerados durante a execução
├── docker-compose.yaml
├── pyproject.toml
├── uv.lock
└── README.md
```

Arquivos com credenciais, logs do Airflow e dados gerados pelo pipeline não são versionados.

## Como executar

### Pré-requisitos

- Docker
- Docker Compose
- Uma chave da API do [OpenWeatherMap](https://openweathermap.org/api)

### 1. Clone o repositório

```bash
git clone https://github.com/NathanCavalcante04/Pipeline_ETL_Weather_Data.git
cd Pipeline_ETL_Weather_Data
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
AIRFLOW_UID=50000
API_KEY=sua_chave_openweathermap
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
user=airflow
password=airflow
database=airflow
host=postgres

# Dependências usadas pelo pipeline dentro dos containers do Airflow.
# Esta opção é adequada para demonstração e desenvolvimento local.
_PIP_ADDITIONAL_REQUIREMENTS=pandas psycopg2-binary python-dotenv requests sqlalchemy pyarrow
```

> O arquivo `.env` contém informações sensíveis e está no `.gitignore`. Nunca publique sua chave real da API.

Em Linux, você pode substituir `50000` pelo seu identificador de usuário:

```bash
id -u
```

### 3. Inicialize o Airflow

```bash
docker compose up airflow-init
```

### 4. Suba os serviços

```bash
docker compose up -d
```

O primeiro início pode demorar alguns minutos porque o Airflow instalará as dependências adicionais.

### 5. Execute a DAG

1. Acesse `http://localhost:8080`.
2. Entre com o usuário e a senha definidos em `_AIRFLOW_WWW_USER_USERNAME` e `_AIRFLOW_WWW_USER_PASSWORD` (no exemplo, `airflow` / `airflow`).
3. Localize a DAG `projeto_weather_pipeline`.
4. Ative a DAG ou inicie uma execução manual.
5. Acompanhe as tarefas `extract`, `transform` e `load` na interface.

Para encerrar os containers:

```bash
docker compose down
```

## Etapas do pipeline

### Extract

Consulta a API OpenWeatherMap para obter as condições meteorológicas atuais de São Paulo. A resposta bruta é salva em `data/weather_data.json`.

### Transform

O Pandas normaliza os campos aninhados do JSON, reorganiza os nomes das colunas, remove campos não utilizados e converte os timestamps para o fuso horário `America/Sao_Paulo`. O resultado intermediário é salvo em `data/temp_data.parquet`.

### Load

O arquivo Parquet é lido e seus registros são inseridos na tabela `sp_weather` do PostgreSQL por meio do SQLAlchemy.

Os dados são transferidos entre as tarefas por arquivos em um volume compartilhado. Isso evita utilizar o XCom para transportar DataFrames, pois ele é mais apropriado para pequenas mensagens e metadados.

## Consultando os dados

O PostgreSQL está exposto localmente na porta `5433`. Um exemplo de consulta é:

```sql
SELECT
    city_name,
    temperature,
    humidity,
    weather_description,
    datetime
FROM sp_weather
ORDER BY datetime DESC;
```

Configuração local da conexão:

```text
Host: localhost
Porta: 5433
Banco: airflow
Usuário: airflow
Senha: airflow
```

As credenciais acima são destinadas somente ao ambiente local de demonstração.

## Decisões técnicas

- O Airflow agenda e monitora as etapas do pipeline.
- O CeleryExecutor distribui as tarefas com Redis como broker.
- JSON preserva a resposta original da API antes das transformações.
- Parquet armazena o resultado intermediário de forma compacta e tipada.
- PostgreSQL permite consultar e consumir os dados processados.
- Volumes do Docker compartilham os arquivos entre as tarefas do Airflow.

## Melhorias futuras

- [ ] Criar uma imagem personalizada do Airflow com as dependências instaladas durante o build
- [ ] Adicionar testes unitários para as transformações
- [ ] Tornar a carga idempotente e impedir registros duplicados
- [ ] Parametrizar cidade e tabela com Airflow Variables
- [ ] Adicionar validações de schema e qualidade dos dados
- [ ] Configurar integração contínua para lint e testes
- [ ] Criar um dashboard para visualizar o histórico meteorológico

## Autor

Nathan Cavalcante da Silva

[LinkedIn](https://linkedin.com/in/nathancavalcante04) · [GitHub](https://github.com/NathanCavalcante04)
