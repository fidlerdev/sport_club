from dotenv import load_dotenv
import os


load_dotenv()

DROP_TABLES = False

BOT_TOKEN = os.environ["BOT_TOKEN"]

USE_MYSQL = os.environ.get("USE_MYSQL", False)

if USE_MYSQL:
    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_NAME = os.environ["DB_NAME"]

    # DATA SOURCE NAME
    DB_DSN = f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DB_DSN = "sqlite:///database.db"
