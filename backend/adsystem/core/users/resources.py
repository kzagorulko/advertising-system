from uuid import uuid4
from validate_email import validate_email

from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, Response
from passlib.hash import pbkdf2_sha256 as sha256

from ..database import db
from ..utils import (
    with_transaction, create_refresh_token, create_access_token, jwt_required,
    make_error, Permissions, validation
)
from ..models import UserModel, RoleModel, PermissionAction
from .utils import (
    is_username_unique, get_role_id, RoleNotExist, get_column_for_order,
)

permissions = Permissions(app_name='users')


class Users(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        users_query = UserModel.outerjoin(RoleModel).select()
        total_query = db.select([db.func.count(UserModel.id)])

        query_params = request.query_params

        if 'search' in query_params:
            users_query.where(
                UserModel.display_name.ilike(f'%{query_params["search"]}%')
            )

        if 'page' in query_params and 'perPage' in query_params:
            page = int(query_params['page']) - 1
            per_page = int(query_params['perPage'])
            users_query = users_query.limit(per_page).offset(page * per_page)

        if 'order' in query_params and 'field' in query_params:
            users_query = users_query.order_by(
                get_column_for_order(
                    query_params['field'],
                    query_params['order'] == 'ASC'
                )
            )

        total = await total_query.gino.scalar()
        users = await users_query.gino.load(
            UserModel.distinct(UserModel.id).load(role=RoleModel)
        ).all()

        return JSONResponse({
            'items': [user.jsonify() for user in users],
            'total': total,
        })

    # TODO make this for admin only
    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.CREATE)
    @validation(schema={
        'username': {
            'required': True,
            'type': str,
            'min_length': 4,
            'max_length': 50,
            'unique_username': True
        },
        'password':  {
            'required': True,
            'type': str,
            'min_length': 5,
            'max_length': 50,
        },
        'displayName': {
            'required': True,
            'type': str,
            'min_length': 5,
            'max_length': 50,
        },
        'email': {
            'required': True,
            'type': str,
            'email': True,
        },
        'role': {
            'required': True,
            'type': str,
            'max_length': 64,
        }
    }, custom_checks={
        'email': {
            # with the pyDNS, it will be better
            'func': lambda v, *args: validate_email(v),
            'message': lambda v, *args: f'`{v}` не является корректной электро'
            f'нной почтой'
        },
        'unique_username': {
            # it works with async functions
            'func': lambda v, *args: is_username_unique(v),
            'message': lambda v, *args: f'Пользователь с `username` `{v}` уже '
            f'существует.'
        },
    })
    async def post(self, data):

        try:
            role_id = await get_role_id(data)
        except RoleNotExist:
            return make_error('Роли не существует', status_code=404)

        new_user = await UserModel.create(
            username=data['username'],
            password=sha256.hash(data['password']),
            session=str(uuid4()),
            display_name=data['displayName'],
            email=data['email'],
            role_id=role_id
        )
        return JSONResponse({'id': new_user.id})


class User(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(request):
        user_id = request.path_params['user_id']
        users = await UserModel.outerjoin(RoleModel).select().where(
            UserModel.id == user_id
        ).gino.load(
            UserModel.distinct(UserModel.id).load(role=RoleModel)
        ).all()
        if users:
            return JSONResponse(users[0].jsonify(for_card=True))
        return make_error(
            f'Пользователь с идентификатором {user_id} не найден',
            status_code=404
        )

    # TODO: make this method for admin only

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE)
    @validation(schema={
        'password': {
            'type': str,
            'min_length': 5,
            'max_length': 30,
        },
        'displayName': {
            'type': str,
            'min_length': 5,
            'max_length': 50,
        },
        'email': {
            'type': str,
            'email': True,
        },
        'role': {
            'type': str,
            'max_length': 64,
        },
        'deactivated': {
            'type': bool
        }
    }, custom_checks={
        'email': {
            # with the pyDNS, it will be better
            'func': lambda v, *args: validate_email(v),
            'message': lambda v, *args: f'`{v}` не является корректной электро'
            f'нной почтой'
        },
        'unique_username': {
            # it works with async functions
            'func': lambda v, *args: is_username_unique(v),
            'message': lambda v, *args: f'Пользователь с `username` `{v}` уже '
            f'существует.'
        },
    }, return_request=True)
    async def patch(self, request, data):
        user_id = request.path_params['user_id']
        user = await UserModel.get(user_id)
        if not user:
            return make_error(
                f'Пользователь с идентификатором {user_id} не найден',
                status_code=404
            )

        try:
            role_id = await get_role_id(data)
        except RoleNotExist:
            return make_error('Роли не существует', status_code=404)

        values = {
            'display_name': data['displayName']
            if 'displayName' in data else None,
            'password': sha256.hash(data['password'])
            if 'password' in data else None,
            'deactivated': data['deactivated']
            if 'deactivated' in data else None,
            'email': data['email'] if 'email' in data else None,
            'role_id': role_id
        }

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        await user.update(**values).apply()

        return Response('', status_code=204)


@validation(schema={
    'identifier': {
        'required': True,
        'type': str,
        'min_length': 4,
        'max_length': 50,
    },
    'password': {
        'required': True,
        'type': str,
        'min_length': 4,
        'max_length': 50,
    },
})
async def get_refresh_token(data):
    user = await UserModel.get_by_identifier(data['identifier'])

    if not user:
        return make_error(
            'Пользователь с таким именем или электронной почтой не найден',
            status_code=404
        )

    if not sha256.verify(data['password'], user.password):
        return make_error('Пароль неверен', status_code=401)

    return JSONResponse({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'refresh_token': create_refresh_token(user.session),
        'access_token': create_access_token(user.session)
    })


@jwt_required(token_type='refresh')
async def get_access_token(request, user):
    return JSONResponse({
        'access_token': create_access_token(user.session),
    })


@jwt_required
@validation(schema={
    'password': {
        'required': True,
        'type': str,
        'min_length': 4,
        'max_length': 50,
    },
})
async def reset_session(data, user):
    if not sha256.verify(data['password'], user.password):
        return make_error('Пароль неверен', status_code=401)

    await user.update(
        session=str(uuid4())
    ).apply()

    return Response('', status_code=204)


@jwt_required
async def get_actions(request, user):
    return JSONResponse(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Users),
    Route('/{user_id:int}', User),
    Route('/actions', get_actions, methods=['GET']),
    Route('/reset-session', reset_session, methods=['POST']),
    Route('/access-tokens', get_access_token, methods=['POST']),
    Route('/refresh-tokens', get_refresh_token, methods=['POST']),
]
