import os
from contextlib import contextmanager
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import Row, select
from sqlmodel import Session, create_engine

from db_work_template.db.model import Documento

load_dotenv(override=True)


DATABASE_URL_MYSQL = os.getenv("DATABASE_URL_MYSQL")
BASEAPI = os.getenv("BASEAPI")
BASEPORTAL = os.getenv("BASEPORTAL")
engine = create_engine(DATABASE_URL_MYSQL + BASEAPI)
my_sql_hml = create_engine(DATABASE_URL_MYSQL + BASEPORTAL)



@contextmanager
def get_session(_engine) -> Generator[Session, None, None]:
    with Session(_engine) as session:
        yield session


def update_escrituracao_status(session: Session, status: bool, mensagem: str, _id: int):
    stmt = select(Documento).where(Documento.id == _id)
    result = session.exec(stmt).first()
    if result:
        if isinstance(result, Row):
            result = result[0]
        try:
            result.status_escrit = status
            result.descri_escrit = mensagem
            session.commit()
            return True
        except Exception as e:
            raise e
    else:
        return False
