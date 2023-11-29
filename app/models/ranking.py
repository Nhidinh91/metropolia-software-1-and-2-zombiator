from app import db


class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    score = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    weapon_remaining = db.Column(db.String(255), nullable=True)
    energy_remaining = db.Column(db.String(255), nullable=True)

    def __init__(self, player_id, score, duration, weapon_remaining, energy_remaining):
        self.player_id = player_id
        self.score = score
        self.duration = duration
        self.weapon_remaining = weapon_remaining
        self.energy_remaining = energy_remaining

    def get_info(self):
        return {
            "id": self.id,
            "player_id": self.player_id,
            "score": self.score,
            "duration": self.duration,
            "weapon_remaining": self.weapon_remaining,
            "energy_remaining": self.energy_remaining,
        }
