import psycopg2
from psycopg2 import Error
import os

# função responsável por criar e retornar a conexão com o banco de dados
def conectar():
    try:
        # tenta conectar usando as variáveis de ambiente definidas no terminal
        # se a variável não estiver definida, usa o valor padrão após a vírgula
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME", "traininglog"), # nome do banco
            user=os.environ.get("DB_USER", "postgres"), # usuario do banco
            password=os.environ.get("DB_PASSWORD"), # senha do banco
            host=os.environ.get("DB_HOST", "localhost"), # endereço do banco
            port=os.environ.get("DB_PORT", "5432") # porta do banco
        )
        return conn # retorna a conexão se tiver sucesso
    
    except Error as e:
        # se der erro retorna a mensagem de erro
        print("Erro ao conectar: ", e)
        return None