from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..database import db
from ..utils import (
    with_transaction, jwt_required, GinoQueryHelper, Permissions, get_date,
    validation, make_list_response, make_response, get_one, make_error,
    NO_CONTENT,
)
from ..models import PermissionAction, CompanyModel
from .utils import validate_date, validate_measure, unique_title

permissions = Permissions(app_name='companies')


class Companies(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        query_params = request.query_params

        current_query = CompanyModel.query
        total_query = db.select([db.func.count(CompanyModel.id)])

        if 'creator_id' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                CompanyModel.creator_id,
                int(query_params['creator_id']),
                current_query,
                total_query
            )

        if 'startStartDate' in query_params:
            current_query, total_query = GinoQueryHelper.month_year_cond(
                CompanyModel.start_date,
                query_params['startStartDate'],
                GinoQueryHelper.GTE,
                current_query,
                total_query
            )
        if 'endStartDate' in query_params:
            current_query, total_query = GinoQueryHelper.month_year_cond(
                CompanyModel.start_date,
                query_params['endStartDate'],
                GinoQueryHelper.LTE,
                current_query,
                total_query
            )

        if 'startEndDate' in query_params:
            current_query, total_query = GinoQueryHelper.month_year_cond(
                CompanyModel.end_date,
                query_params['startEndDate'],
                GinoQueryHelper.GTE,
                current_query,
                total_query
            )
        if 'endEndDate' in query_params:
            current_query, total_query = GinoQueryHelper.month_year_cond(
                CompanyModel.end_date,
                query_params['endEndDate'],
                GinoQueryHelper.LTE,
                current_query,
                total_query
            )

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )
        current_query = GinoQueryHelper.order(
            query_params,
            current_query, {
                'id': CompanyModel.id,
                'creator_id': CompanyModel.creator_id,
                'start_date': CompanyModel.start_date,
                'end_date': CompanyModel.end_date,
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
    @permissions.required(action=PermissionAction.CREATE, return_user=True)
    @validation(schema={
        'title': {
            'required': True,
            'type': str,
            'min_length': 3,
            'max_length': 50,
            'title': True,
        },
        'startDate': {
            'required': True,
            'type': str,
            'date': True,
        },
        'endDate': {
            'required': True,
            'type': str,
            'date': True,
        },
        'exceptedProfit': {
            'required': True,
            'type': (float, int),
        },
        'measureId': {
            'required': True,
            'type': int,
            'measure': True,
        },
    }, custom_checks={
        'date': {
            'func': validate_date,
            'message': lambda *args: 'Неизвестный формат даты. Пример: 2020-12'
            '-31;'
        },
        'measure': {
            'func': validate_measure,
            'message': lambda v, *args: f'Единцы измерения с id {v} не существ'
            f'ует.'
        },
        'title': {
            'func': unique_title,
            'message': lambda v, *args: f'Название {v} не уникально.'
        },
    })
    async def post(self, data, user):
        new_company = await CompanyModel.create(
            start_date=get_date(data['startDate']),
            end_date=get_date(data['endDate']),
            excepted_profit=data['exceptedProfit'],
            profit=0,
            measure_id=data['measureId'],
            creator_id=user.id,
            title=data['title'],
        )

        return make_response({'id': new_company.id})


class Company(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        return await get_one(
            CompanyModel,
            request.path_params['company_id'],
            'Рекламная компания'
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'title': {
            'type': str,
            'min_length': 3,
            'max_length': 50,
            'title': True,
        },
        'startDate': {
            'type': str,
            'date': True,
        },
        'endDate': {
            'type': str,
            'date': True,
        },
        'profit': {
            'type': (float, int),
        },
        'measureId': {
            'type': int,
            'measure': True,
        },
    }, custom_checks={
        'date': {
            'func': validate_date,
            'message': lambda *args: 'Неизвестный формат даты. Пример: 2020-12'
            '-31;'
        },
        'measure': {
            'func': validate_measure,
            'message': lambda v, *args: f'Единцы измерения с id {v} не существ'
            f'ует.'
        },
        'title': {
            'func': unique_title,
            'message': lambda v, *args: f'Название {v} не уникально.',
            'request': True,
        },
    }, return_request=True)
    async def patch(self, request, data):
        company_id = request.path_params['company_id']

        company = await CompanyModel.get(company_id)

        if not company:
            return make_error(
                f'Рекламная компания с id {company_id} не найдена',
                status_code=404
            )

        values = {
            'start_date': get_date(data['startDate'])
            if 'startDate' in data else None,
            'end_date': get_date(data['endDate'])
            if 'endDate' in data else None,
            'profit': data['profit'] if 'profit' in data else None,
            'measure_id': data['measureId'] if 'measureId' in data else None,
            'title': data['title'] if 'title' in data else None,
        }

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        await company.update(**values).apply()

        return NO_CONTENT


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))

routes = [
    Route('/', Companies),
    Route('/{company_id:int}', Company),
    Route('/actions', get_actions, methods=['GET']),
]
