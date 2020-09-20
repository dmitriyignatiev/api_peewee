from aiohttp import web
from graphene import ObjectType
from graphene_peewee_async.fields import PeeweeConnectionField, PeeweeConnection
from graphene_peewee_async.types import PeeweeObjectType

from main import objects
from sales.db import db
from sales.db.db import TestModel


async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.question.select())
        records = await cursor.fetchall()
        print(records)
        questions = [dict(q) for q in records]

        return web.Response(text=str(questions))

async def new_index(request):
        # await objects.create(TestModel, text="!!!Not bad. Watch this, I'm async!")
        all_objects = await objects.execute(TestModel.select())
        for obj in all_objects:
            print(obj.text, obj.id)
        print(all_objects.__dict__)
        # d = [dict(q) for q in all_objects._rows]
        return web.Response(text='hjhjjh')


from sales.db.db import TestModel






import graphene
import asyncio
from graphql.execution.executors.asyncio import AsyncioExecutor

from aiohttp_graphql import GraphQLView
# from info.api.queries import Query
# from info.api.mutations import Mutations


class AuthorNode(PeeweeObjectType):
    class Meta:
        model = TestModel
        manager = objects

class AuthorConnection(PeeweeConnection):
    class Meta:
        node = AuthorNode

class Query(ObjectType):
    books = PeeweeConnectionField(AuthorConnection)

schema = graphene.Schema(
    query=Query,
    # mutation=Mutations
)

gqil_view = GraphQLView(
    schema=schema,
    executor=AsyncioExecutor(loop=asyncio.get_event_loop()),
    graphiql=True,
    enable_async=True,
)

gql_view = GraphQLView(
    schema=schema,
    executor=AsyncioExecutor(loop=asyncio.get_event_loop()),
    graphiql=False,
    enable_async=True,
)