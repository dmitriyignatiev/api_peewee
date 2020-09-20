import datetime
from peewee import *

from sales.db.db import database

class BaseModel(Model):
    class Meta:
        database = database





class Parent(BaseModel):
    name = TextField()


class Child(BaseModel):
    name = TextField()
    # parent = ForeignKeyField(Parent, backref='childs')

class Table(BaseModel):
    child = ForeignKeyField(Child, backref='table')
    parent = ForeignKeyField(Parent, backref='table')

def populate_data():
    database.create_tables([Child, Parent, Table])

populate_data()


x = Parent.select().join(Table).where(Table.child == 1)

for i in x:
    print(i.name)
# parent = Parent.create(name='Dima')
# child = Child.create(name='Masha')
# parent = Parent.select().where(Parent.name == 'Dima').get()

