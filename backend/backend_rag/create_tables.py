import asyncio
from db.neon_connector import NeonConnector
from db.models import Base

async def main():
    db = NeonConnector()

    # Tables create
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Neon DB tables created successfully!")
    await db.close_connection()

if __name__ == "__main__":
    asyncio.run(main())