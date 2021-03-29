from ..utils import get_date
from ..models import MeasureModel, CompanyModel


def validate_date(v, *args):
    try:
        get_date(v)
        return True
    except ValueError:
        return False


async def validate_measure(v, *args):
    measure = await MeasureModel.get(v)
    return bool(measure)


async def unique_title(v, *args, request=None):
    company = await CompanyModel.query.where(
        CompanyModel.title == v
    ).gino.first()

    return not bool(company) or request.path_params['company_id'] == company.id
