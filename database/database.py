from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

import config


engine = create_engine(url=config.DB_DSN, echo=True)
session_factory = sessionmaker(bind=engine)


class Base(DeclarativeBase): ...