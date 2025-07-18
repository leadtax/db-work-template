from contextlib import contextmanager
import os

from typing import Generator


from db_work_template.db.model import Documento
from sqlmodel import Session, create_engine, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv(override=True)


DATABASE_URL_MYSQL = os.getenv("DATABASE_URL_MYSQL")
BASEAPI = os.getenv("BASEAPI")
BASEPORTAL = os.getenv("BASEPORTAL")
engine = create_engine(DATABASE_URL_MYSQL + BASEAPI)
my_sql_hml = create_engine(DATABASE_URL_MYSQL + BASEPORTAL)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@contextmanager
def get_session(_engine) -> Generator[Session, None, None]:
    with Session(_engine) as session:
        yield session


def update_escrituracao_status(session: Session, status: bool, mensagem: str, _id: int):
    stmt = select(Documento).where(Documento.id == _id)
    result = session.exec(stmt).first()
    if result:
        try:
            result.status_escrit = status
            result.descri_escrit = mensagem
            session.commit()
            return True
        except Exception as e:
            raise e
    else:
        return False
