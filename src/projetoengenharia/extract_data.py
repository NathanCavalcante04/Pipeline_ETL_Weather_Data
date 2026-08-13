import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




def extract_weather_data(
    url: str,
    output_path: str | Path = "data/weather_data.json",
) -> dict:

    response = requests.get(url, timeout=30)
    data = response.json()
    print(response.status_code)

    if response.status_code != 200:
        logging.error("ERRO na requisição")
        return []

    if not data:
        logging.warning("Nenhum dado retornado")
        return []

    output_path = Path(output_path)
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    logging.info(f"arquivo salvo em {output_path}")

    return data

