import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db_work_template.db.model import Documento

load_dotenv(override=True)

DATABASE_URL_MYSQL = os.getenv("DATABASE_URL_MYSQL").replace("pymysql", "aiomysql")
BASEAPI = os.getenv("BASEAPI").replace("pymysql", "aiomysql")
BASEPORTAL = os.getenv("BASEPORTAL").replace("pymysql", "aiomysql")

engine = create_async_engine(DATABASE_URL_MYSQL + BASEAPI, echo=False)
my_sql_hml = create_async_engine(DATABASE_URL_MYSQL + BASEPORTAL, echo=False)


@asynccontextmanager
async def get_async_session(
    _engine: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        _engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def update_escrituracao_status_async(
    session: AsyncSession, status: bool, mensagem: str, _id: int
):
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
