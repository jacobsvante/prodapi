from prodapi import ProdAPI

from .routes import make_router
from .sec import setup_security

security = setup_security()

app = ProdAPI().with_user_routes(security).with_health_routes().with_basic_cors()

app.include_router(make_router(security))
