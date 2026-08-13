# from src.projetoengenharia.extract_data import extract_weather_data
# from src.projetoengenharia.load_data import load_weather_data
# from src.projetoengenharia.transform_data import data_transformations

# import os
# from pathlib import Path
# from dotenv import load_dotenv

# import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# env_path = Path(__file__).resolve().parent / "config" / ".env"
# load_dotenv(env_path)

# API_KEY = os.getenv("API_KEY")

# url = (
#     "https://api.openweathermap.org/data/2.5/weather"
#     f"?q=Sao Paulo,BR&units=metric&appid={API_KEY}"
# )
# table_name = 'sp_weather'

# def pipeline():

#     try:
#         logging.info("ETAPA 1: EXTRACT")
#         extract_weather_data(url)

#         logging.info("ETAPA 2: TRANSFORM")
#         df = data_transformations()

#         logging.info("ETAPA 3 :LOAD")
#         load_weather_data(table_name, df)

#         print("pipeline concluido com sucesso")

#     except Exception:
#         logging.exception("Erro no pipeline")


# if __name__ == "__main__":
#     pipeline()
