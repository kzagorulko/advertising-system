from json import loads
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..database import db
from ..utils import (
    Permissions, jwt_required, GinoQueryHelper, make_list_response,
    with_transaction, validation, make_response, get_one, NO_CONTENT,
    make_error,
)
from ..models import PermissionAction, BannerTypeModel
from .utils import unique_name
from .models import PrimaryBannerType

permissions = Permissions(app_name='banner_types')


class BannerTypes(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        query_params = request.query_params

        current_query = BannerTypeModel.query
        total_query = db.select([db.func.count(BannerTypeModel.id)])

        if 'name' in query_params:
            current_query, total_query = GinoQueryHelper.search(
                BannerTypeModel.creator_id,
                query_params['name'],
                current_query,
                total_query
            )

        if 'id' in query_params:
            current_query, total_query = GinoQueryHelper.in_(
                BannerTypeModel.id,
                loads(query_params['id']),
                current_query,
                total_query
            )

        if 'primaryType' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                BannerTypeModel.primary_type,
                query_params['primaryType'],
                current_query,
                total_query
            )

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )
        current_query = GinoQueryHelper.order(
            query_params,
            current_query, {
                'id': BannerTypeModel.id,
                'name': BannerTypeModel.name,
                'primaryType': BannerTypeModel.primary_type,
            }
        )

        total = await total_query.gino.scalar()
        items = await current_query.gino.all()

        return make_list_response(
            [item.jsonify() for item in items],
            total
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.CREATE)
    @validation(schema={
        'name': {
            'required': True,
            'type': str,
            'min_length': 1,
            'max_length': 30,
            'name': True,
        },
        'primaryType': {
            'required': True,
            'type': str,
            'min_length': 1,
            'max_length': 15,
            'primary_type': True,
        }
    }, custom_checks={
        'name': {
            'func': unique_name,
            'message': lambda v, *args: f'Тип с именем `{v}` уже существует.',
        },
        'primary_type': {
            'func': lambda v, *args: v in PrimaryBannerType.__members__.keys(),
            'message': lambda v, *args: f'Основного типа `{v}` не существует',
        }
    })
    async def post(self, data):
        new_type = await BannerTypeModel.create(
            name=data['name'], primary_type=data['primaryType']
        )
        return make_response({'id': new_type.id})


class BannerType(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        return await get_one(
            BannerTypeModel,
            request.path_params['banner_type_id'],
            'Тип баннера'
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'name': {
            'required': True,
            'type': str,
            'min_length': 1,
            'max_length': 30,
            'name': True,
        },
        'primaryType': {
            'required': True,
            'type': str,
            'min_length': 1,
            'max_length': 15,
            'primary_type': True,
        }
    }, custom_checks={
        'name': {
            'func': unique_name,
            'message': lambda v, *args: f'Тип с именем `{v}` уже существует.',
        },
        'primary_type': {
            'func': lambda v, *args: v in PrimaryBannerType.__members__.keys(),
            'message': lambda v, *args: f'Основного типа `{v}`` не существует',
        }
    }, return_request=True)
    async def patch(self, request, data):
        banner_type_id = request.path_params['banner_type_id']
        banner_type = await BannerTypeModel.get(banner_type_id)
        if not banner_type:
            return make_error(
                f'Тип баннера с идентификатором {banner_type_id} не найден',
                status_code=404
            )

        values = {
            'name': data['name'] if 'name' in data else None,
            'primary_type': data['primaryType']
            if 'primaryType' in data else None,
        }

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        await banner_type.update(**values).apply()

        return NO_CONTENT


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))

routes = [
    Route('/', BannerTypes),
    Route('/{banner_type_id:int}', BannerType),
    Route('/actions', get_actions, methods=['GET']),
]
