import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Carrega as variáveis existentes no arquivo .env
load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# Verifica se as configurações obrigatórias foram informadas
if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
    raise RuntimeError(
        "As configurações do banco não foram encontradas no arquivo .env."
    )


# Protege caracteres especiais existentes na senha
senha_codificada = quote_plus(DB_PASSWORD)


DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{senha_codificada}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    banco = SessionLocal()

    try:
        yield banco
    finally:
        banco.close()