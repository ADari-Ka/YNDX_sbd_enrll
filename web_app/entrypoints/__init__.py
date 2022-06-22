from fastapi_app import app
from routers import nodes

app.include_router(nodes.router)
