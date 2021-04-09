from prodapi import ProdAPI

from .auth import security
from .routes import router

__all__ = ("app",)

app = ProdAPI(title="{{ project_name }}")

app.with_user_routes(security)
app.with_health_routes()
app.with_basic_cors()

app.include_router(router)
