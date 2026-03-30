import psycopg2
from psycopg2 import Error
import os

def conectar():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME", "traininglog"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST", "localhost"),
            port=os.environ.get("DB_PORT", "5432")
        )
        return conn
    except Error as e:
        print("Erro ao conectar: ", e)
        return None