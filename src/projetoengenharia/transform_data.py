import json
import logging
from os import PathLike
from pathlib import Path

import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "weather_data.json"
columns_names_to_drop = ['weather', 'weather_icon', 'sys.type']
columns_names_to_rename = {
   "name": "city_name",
    "cod": "code",
    "dt": "datetime",
    "coord.lon": "longitude",
    "coord.lat": "latitude",
    "main.temp": "temperature",
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "main.sea_level": "sea_level",
    "main.grnd_level": "grnd_level",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "wind.gust": "wind_gust",
    "clouds.all": "clouds",
    "sys.type": "sys_type",
    "sys.id": "sys_id",
    "sys.country": "country",
    "sys.sunrise": "sunrise",
    "sys.sunset": "sunset",
# weather.id, weather_main, weather_description
}
columns_to_normalize_datetime = ['datetime', 'sunrise', 'sunset']

def create_dataframe(
    path_name: str | PathLike[str] = DEFAULT_DATA_PATH,
) -> pd.DataFrame:
    """Carrega o JSON meteorologico em um DataFrame."""
    path = Path(path_name)
    


    if not path.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    df = pd.json_normalize(data)
    logging.info("DataFrame criado com %d linha(s)", len(df))
    return df


def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, df_weather], axis=1)

    logging.info(f"\n coluna 'weather' normalizada - {len(df.columns)} colunas" )

    return df


def drop_columns(df:pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    logging.info(f"\n removendo colunas: {columns_names}")
    df = df.drop(columns=columns_names)
    logging.info(f"colunas removidas - {len(df.columns)} colunas restantes")
    return df

def rename_columns(df:pd.DataFrame, columns_names:dict[str, str]) -> pd.DataFrame:
    df = df.rename(columns=columns_names)
    return df


def normalize_datetime_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:

    for name in columns_names:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')

    return df

def data_transformations(
    path_name: str | PathLike[str] = DEFAULT_DATA_PATH,
) -> pd.DataFrame:
    print("\n iniciando transformações")
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, columns_names_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    logging.info("transformações concluidas")
    return df 
