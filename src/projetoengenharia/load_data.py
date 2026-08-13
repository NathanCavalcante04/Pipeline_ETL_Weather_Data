from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

env_path = Path(__file__).resolve().parents[2] / 'config' / '.env'
load_dotenv(env_path)

user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')
host = os.getenv('host', 'postgres')

def get_engine():
    logging.info(f"conectando em {host}:5432/{database}")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
    )

def load_weather_data(table_name:str, df):
    engine = get_engine()
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index= False
    )

    logging.info(f"dados carregados com sucesso")

    df_check = pd.read_sql(f'SELECT * FROM {table_name}', con=engine)
    logging.info(f"total de registros na tabela:{len(df_check)}")
