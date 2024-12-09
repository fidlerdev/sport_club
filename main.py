import asyncio
import logging
import config
from database.query import create_tables, drop_tables
from bot import start_bot


async def main():
    if config.DROP_TABLES:
        drop_tables()
    create_tables()
    await start_bot()

    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
