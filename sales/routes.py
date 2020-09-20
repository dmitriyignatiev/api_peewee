import aiohttp_cors

from sales.views import index, new_index
from sales.views import gqil_view, gql_view

def setup_routes(app, cors):
    app.router.add_get('/', index)
    app.router.add_get('/new', new_index )

    resource = cors.add(app.router.add_resource("/graphql"), {
        "*": aiohttp_cors.ResourceOptions(
            expose_headers="*",
            allow_headers="*",
            allow_credentials=True,
            allow_methods=["POST", "PUT", "GET"]),
    })
    resource.add_route("POST", gql_view)
    resource.add_route("PUT", gql_view)
    resource.add_route("GET", gql_view)