from ..database import db


class CompanyModel(db.Model):
    __tablename__ = 'advertising_companies'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    excepted_profit = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(50), nullable=False, unique=True,)
    measure_id = db.Column(
        db.Integer, db.ForeignKey('measures.id'), nullable=False
    )
    creator_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )

    def jsonify(self, for_card=False):
        result = {
            'id': self.id,
            'title': self.title,
            'startDate': self.start_date.isoformat(),
            'endDate': self.end_date.isoformat(),
            'creatorId': self.creator_id,
        }
        if for_card:
            result['measureId'] = self.measure_id
            result['exceptedProfit'] = self.excepted_profit
            result['profit'] = self.profit
        return result
