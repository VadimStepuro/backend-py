from app.configs.db_config import engine
from app.model.models import Base
from dotenv import load_dotenv
from asyncio import run


async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    load_dotenv()
    run(create_tables())
