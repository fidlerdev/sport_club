import asyncio
import logging
import config
from database.queries import create_tables, drop_tables
from bot import start_bot


async def main():
    # create_tables()
    if config.DROP_TABLES:
        drop_tables()
    await start_bot()

    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())