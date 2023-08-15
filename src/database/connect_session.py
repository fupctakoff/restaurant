from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from src.database.models import Base

CONNECTION = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

engine = create_engine(CONNECTION)
engine.connect()

# создание таблиц в бд на основе моделей
Base.metadata.create_all(engine)

# создание сессии для изменений в бд
Session = sessionmaker(bind=engine)
session = Session()