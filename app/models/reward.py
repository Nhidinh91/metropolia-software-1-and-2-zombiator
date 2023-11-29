from app import db


class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    difficult_level = db.Column(db.String(40), nullable=True)
    passing_condition = db.Column(db.Integer, nullable=True)

    def __init__(self, name, amount, difficult_level, passing_condition):
        self.name = name
        self.amount = amount
        self.difficult_level = difficult_level
        self.passing_condition = passing_condition

    def get_info(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "difficult_level": self.difficult_level,
            "passing_condition": self.passing_condition
        }
