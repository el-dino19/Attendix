import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    DATABASE_URL = os.getenv('DATABASE_URL')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY')