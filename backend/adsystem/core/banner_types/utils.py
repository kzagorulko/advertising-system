from ..models import BannerTypeModel


async def unique_name(name, *args):
    type_model = await BannerTypeModel.query.where(
        BannerTypeModel.name == name
    ).gino.first()

    return not type_model
