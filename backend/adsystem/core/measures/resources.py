from json import loads
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from ..utils import (
    jwt_required, Permissions, GinoQueryHelper, make_list_response, get_one,
    with_transaction, validation, make_response, NO_CONTENT,
)
from ..models import PermissionAction, MeasureModel
from ..database import db

permissions = Permissions(app_name='companies')


class Measures(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        query_params = request.query_params

        current_query = MeasureModel.query
        total_query = db.select([db.func.count(MeasureModel.id)])

        if 'search' in query_params:
            current_query, total_query = GinoQueryHelper.search(
                MeasureModel.name,
                query_params['search'],
                current_query,
                total_query
            )

        if 'id' in query_params:
            current_query, total_query = GinoQueryHelper.in_(
                MeasureModel.id,
                loads(query_params['id']),
                current_query,
                total_query
            )

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )
        current_query = GinoQueryHelper.order(
            query_params,
            current_query, {
                'id': MeasureModel.id,
                'name': MeasureModel.name
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
        }
    })
    async def post(self, data):
        new_measure = await MeasureModel.create(name=data['name'])
        return make_response({'id': new_measure.id})


class Measure(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        return await get_one(
            MeasureModel, request.path_params['measure_id'], 'Меры'
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
        }
    }, return_request=True)
    async def patch(self, data, request):
        measure_id = request.path_params['measure_id']
        measure = await MeasureModel.get(measure_id)
        await measure.update(name=data['name']).apply()
        return NO_CONTENT


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Measures),
    Route('/{measure_id:int}', Measure),
    Route('/actions', get_actions, methods=['GET']),
]
