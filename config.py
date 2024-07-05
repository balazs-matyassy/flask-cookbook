import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME = os.environ.get('APP_NAME')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ALCHEMICAL_DATABASE_URL = os.environ.get('ALCHEMICAL_DATABASE_URL')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 4 * 1024 * 1024)
