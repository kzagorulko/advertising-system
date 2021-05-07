from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

from .users.resources import routes as user_routes
from .roles.resources import routes as roles_routes
from .measures.resources import routes as measure_routes
from .companies.resources import routes as company_routes
from .banner_types.resources import routes as banner_types_routes
from .permissions.resources import get_apps


async def ping(request):
    return JSONResponse({'onPing': 'wePong'})

routes = [
    Route('/ping', ping),
    Route('/apps', get_apps, methods=['GET']),
    Mount('/users', routes=user_routes),
    Mount('/roles', routes=roles_routes),
    Mount('/measures', routes=measure_routes),
    Mount('/companies', routes=company_routes),
    Mount('/bannerTypes', routes=banner_types_routes)
]
