# TrainingLog

Sistema de registro de treinos com Python e PostgreSQL.

## Requisitos

- Python 3.x
- PostgreSQL

## Instalação

1. Clone o repositório:
git clone https://github.com/ALLANln/TrainingLog

2. Instale as dependências:
pip install psycopg2

3. Crie o banco de dados no PostgreSQL:
CREATE DATABASE traininglog;

4. Crie a tabela:
CREATE TABLE treinos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(100),
    data DATE,
    duracao INTEGER,
    intensidade VARCHAR(50)
);

## Como rodar

1. Defina a senha do banco no terminal:

Windows:
set DB_PASSWORD=sua_senha

Linux/Mac:
export DB_PASSWORD=sua_senha

2. Rode o projeto:
python main.py
