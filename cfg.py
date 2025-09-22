import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
SECRET_API =os.getenv("SECRET_API")
BASE_URL_TEST = os.getenv("BASE_URL_TEST")
BASE_URL =os.getenv("BASE_URL")
KLINE_ENDPOINT = os.getenv("KLINE_ENDPOINT")
