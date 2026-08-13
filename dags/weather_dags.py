import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow.sdk import dag, task
from dotenv import load_dotenv


sys.path.insert(0, "/opt/airflow/src")

from projetoengenharia.extract_data import extract_weather_data
from projetoengenharia.load_data import load_weather_data
from projetoengenharia.transform_data import data_transformations


DATA_DIR = Path("/opt/airflow/data")
RAW_DATA_PATH = DATA_DIR / "weather_data.json"
TRANSFORMED_DATA_PATH = DATA_DIR / "temp_data.parquet"

env_path = Path("/opt/airflow/config/.env")
load_dotenv(env_path)


@dag(
    dag_id="projeto_weather_pipeline",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    description="Pipeline ETL - Clima de Sao Paulo",
    schedule="0 * * * *",
    start_date=datetime(2026, 8, 13),
    catchup=False,
    tags=["weather", "etl"],
)
def weather_pipeline():
    @task
    def extract():
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("A variavel de ambiente API_KEY nao foi configurada")

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q=Sao Paulo,BR&units=metric&appid={api_key}"
        )
        extract_weather_data(url, output_path=RAW_DATA_PATH)

    @task
    def transform():
        df = data_transformations(RAW_DATA_PATH)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        df.to_parquet(TRANSFORMED_DATA_PATH, index=False)

    @task
    def load():
        import pandas as pd

        df = pd.read_parquet(TRANSFORMED_DATA_PATH)
        load_weather_data("sp_weather", df)

    extract() >> transform() >> load()


weather_pipeline()
