from sqlalchemy import create_engine, MetaData
from sales.db.db import question

from dynaconf import settings


DSN = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NASE}"

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[question])

def sample_data(engine):
    conn = engine.connect()
    conn.execute(question.insert(), [
        {'question_text': 'What\'s new?',
         'pub_date': '2015-12-15 17:17:49.629+02'}
    ])
    conn.close()

if __name__ == '__main__':
    engine = create_engine(DSN)
    create_tables(engine)
    sample_data(engine)
