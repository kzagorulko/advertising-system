from ..database import db


class MeasureModel(db.Model):
    __tablename__ = 'measures'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def jsonify(self, **kwargs):
        return {
            'id': self.id,
            'name': self.name,
        }
