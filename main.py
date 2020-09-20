import asyncio

import aiohttp_cors
import peewee_async
from aiohttp import web

from sales.db.db import init_pg, close_pg, TestModel, database
from sales import routes


from dynaconf import settings



async def init_app():

    app = web.Application()
    cors = aiohttp_cors.setup(app)
    routes.setup_routes(app, cors)

    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)




    return app

app = init_app()
objects = peewee_async.Manager(database)

# async def handler():
#     await objects.create(TestModel, text="dsdd bad. Watch this, I'm async!")
#     all_objects = await objects.execute(TestModel.select())
#     for obj in all_objects:
#         print(obj.text)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(handler())
# loop.close()



if __name__=='__main__':
    # loop = asyncio.get_event_loop()
    app  = init_app()

    web.run_app(app, port=settings.get('AIO_PORT'))