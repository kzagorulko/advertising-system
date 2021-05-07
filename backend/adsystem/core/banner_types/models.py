from enum import Enum
from ..database import db


class PrimaryBannerType(Enum):
    HUMAN = 0
    STATIC = 1


class BannerTypeModel(db.Model):
    __tablename__ = 'banner_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    primary_type = db.Column(db.Enum(PrimaryBannerType), nullable=False)

    def jsonify(self, **kwargs):
        return {
            'id': self.id,
            'name': self.name,
            'primaryType': self.primary_type.name,
        }
