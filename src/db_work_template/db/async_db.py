from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from db_work_template.db.model import Documento

import os
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URL_MYSQL = os.getenv("DATABASE_URL_MYSQL")
BASEAPI = os.getenv("BASEAPI")
BASEPORTAL = os.getenv("BASEPORTAL")

engine = create_async_engine(DATABASE_URL_MYSQL + BASEAPI, echo=False)
my_sql_hml = create_async_engine(DATABASE_URL_MYSQL + BASEPORTAL, echo=False)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_async_session(_engine) -> AsyncGenerator[AsyncSession, None, None]:
    async_session = sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

async def update_escrituracao_status_async(session: AsyncSession, status: bool, mensagem: str, _id: int):
    try:
        stmt = select(Documento).where(Documento.id == _id)
        result = await session.execute(stmt)
        documento = result.scalars().first()

        if documento:
            documento.status_escrit = status
            documento.descri_escrit = mensagem
            await session.commit()
            return True
        else:
            return False
    except Exception as e:
        await session.rollback()
        raise e
