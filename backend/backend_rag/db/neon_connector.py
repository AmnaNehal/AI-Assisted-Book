from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config.settings import settings
import logging

import ssl
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

logger = logging.getLogger(__name__)


def _clean_db_url(url: str) -> str:
    """
    .env ko touch kiye baghair URL me se sslmode / channel_binding remove karta hai,
    aur asyncpg ke liye SSL connect_args me set karta hai.
    """
    p = urlparse(url)
    qs = dict(parse_qsl(p.query))
    qs.pop("sslmode", None)
    qs.pop("channel_binding", None)
    new_q = urlencode(qs, doseq=True)
    return urlunparse(p._replace(query=new_q))


class NeonConnector:
    """
    Connector class for interacting with Neon Serverless Postgres database
    """

    def __init__(self):
        db_url = _clean_db_url(settings.NEON_DB_URL)
        ssl_ctx = ssl.create_default_context()

        self.engine = create_async_engine(
            db_url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args={"ssl": ssl_ctx},
        )

        self.async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def test_connection(self):
        """
        Test the database connection
        """
        try:
            async with self.async_session() as session:
                await session.execute(text("SELECT 1"))
                logger.info("Database connection test successful")
                return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

    async def close_connection(self):
        """
        Close the database connection pool
        """
        await self.engine.dispose()
        logger.info("Database connection closed")