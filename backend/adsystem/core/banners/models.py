from enum import Enum
from ..database import db


class BannerStatus(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    CANCELLED = 2
    DONE = 3


class BannerModel(db.Model):
    __tablename__ = 'banners'

    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    coordinates = db.Column(db.String(21), nullable=False)
    status = db.Column(db.Enum(BannerStatus), nullable=False)
    advertising_company_id = db.Column(
        db.Integer, db.ForeignKey('advertising_companies.id'), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    banner_type_id = db.Column(
        db.Integer, db.ForeignKey('banner_types.id'), nullable=False
    )
