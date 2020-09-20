import aiopg
import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

from dynaconf import settings
meta = MetaData()

question = Table(
    'question', meta,

    Column('id', Integer, primary_key=True),
    Column('question_text', String(200), nullable=False),
    Column('pub_date', Date, nullable=False)
)

import asyncio
import peewee
import peewee_async

DATABASE = {
    'database': settings['DB_NAME'],
    'password': settings['DB_PASSWORD'],
    'user': settings['DB_USER'],
    'host': settings['DB_HOST'],
    'port': settings['DB_PORT']
}

database = peewee_async.PostgresqlDatabase(
    ** DATABASE

)

class TestModel(peewee.Model):
    text = peewee.CharField()

    class Meta:
        database = database


class Author(peewee.Model):
    name = peewee.CharField()
    rating=peewee.IntegerField(default=1)

    class Meta:
        database = database

class Book(peewee.Model):
    name =peewee.CharField()
    year = peewee.IntegerField()
    author = peewee.ForeignKeyField(Author)

    class Meta:
        database = database




# Author.create_table(True)
# Book.create_table(True)

# Author.create(name="First_author")
# Book.create(name='Firsr_book', year=1995)


database.close()

objects = peewee_async.Manager(database)

async def init_pg(app):
    engine = await aiopg.sa.create_engine(
        database=settings['DB_NAME'],
        user=settings['DB_USER'],
        password=settings['DB_PASSWORD'],
        host=settings['DB_HOST'],
        port=settings['DB_PORT'],
    )
    database.init(**DATABASE)
    app.database = database
    app.objects = peewee_async.Manager(app.database)
    app['db'] = engine



async def close_pg(app):
    app['db'].close()
    database.close()
    await app['db'].wait_closed()