from src.config import settings
from sqlalchemy import  create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_engine(
    settings.DATABASE_URL_psycopg
)


async_engine = create_async_engine(
    settings.DATABASE_URL_asyncpg
)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


