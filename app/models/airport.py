from app import db


class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(40), nullable=False, unique=True)
    name = db.Column(db.String(40), nullable=True)
    latitude_deg = db.Column(db.Float, nullable=True)
    longitude_deg = db.Column(db.Float, nullable=True)
    continent = db.Column(db.String(40), nullable=True)
    country = db.Column(db.String(40), nullable=True)
    stage = db.Column(db.Integer, nullable=True) # 0: normal, 1: base, 2: boss

    def __init__(self, ident, name, latitude_deg, longitude_deg, continent, country, stage):
        self.ident = ident
        self.name = name
        self.latitude_deg = latitude_deg
        self.longitude_deg = longitude_deg
        self.continent = continent
        self.country = country
        self.stage = stage

    def get_info(self):
        return {
            "id": self.id,
            "ident": self.ident,
            "name": self.name,
            "latitude_deg": self.latitude_deg,
            "longitude_deg": self.longitude_deg,
            "continent": self.continent,
            "country": self.country,
            "stage": self.stage,
        }
