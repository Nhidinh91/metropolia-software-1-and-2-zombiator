from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(40), default="Finland")
    inventory_weapon = db.Column(db.Integer, nullable=False, default=0)
    inventory_energy = db.Column(db.Integer, nullable=False, default=0)
    game_status = db.Column(db.String(40), nullable=False, default="not_started")
    game_master_password = db.Column(db.String(255), nullable=True)
    game_master_password_retry_times = db.Column(db.Integer, nullable=True, default=0)
    game_start_at = db.Column(db.DateTime, nullable=True)
    game_actual_end_at = db.Column(db.DateTime, nullable=True)
    game_end_at = db.Column(db.DateTime, nullable=True)
    game_paused_at = db.Column(db.DateTime, nullable=True)
    game_password_collected = db.Column(db.String(255), nullable=True)
    game_completed_airports = db.Column(db.String(255), nullable=True)

    def __init__(
        self,
        name,
        email,
        password,
        location="Finland",
        inventory_weapon=200,
        inventory_energy=500,
        game_status="not_started",
        game_master_password="",
        game_master_password_retry_times=0,
        game_start_at=None,
        game_end_at=None,
        game_actual_end_at=None,
        game_paused_at=None,
        game_password_collected="",
        game_completed_airports="",
    ):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.location = location
        self.inventory_weapon = inventory_weapon
        self.inventory_energy = inventory_energy
        self.game_status = game_status
        self.game_master_password = game_master_password
        self.game_master_password_retry_times = game_master_password_retry_times
        self.game_start_at = game_start_at
        self.game_end_at = game_end_at
        self.game_actual_end_at = game_actual_end_at
        self.game_paused_at = game_paused_at
        self.game_password_collected = game_password_collected
        self.game_completed_airports = game_completed_airports

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "location": self.location,
            "inventory_weapon": self.inventory_weapon,
            "inventory_energy": self.inventory_energy,
            "game_status": self.game_status,
            "game_start_at": self.game_start_at,
            "game_end_at": self.game_end_at,
            "game_actual_end_at": self.game_actual_end_at,
            "game_paused_at": self.game_paused_at,
            "game_password_collected": self.game_password_collected,
            "game_completed_airports": self.game_completed_airports,
            "game_master_password_retry_times" : self.game_master_password_retry_times,
        }

    def get_game_status(self):
        return self.game_status

    def format_date(self, date_attribute):
        return date_attribute.strftime("%Y-%m-%d %H:%M:%S") if date_attribute else None

    def get_game_start_at(self):
        return self.format_date(self.game_start_at)

    def get_game_end_at(self):
        return self.format_date(self.game_end_at)

    def get_game_password_collected(self):
        return self.game_password_collected

    def get_game_completed_airports(self):
        return self.game_completed_airports

    def set_game_status(self, game_status):
        self.game_status = game_status

    def set_game_start_at(self, game_start_at):
        self.game_start_at = game_start_at

    def set_game_end_at(self, game_end_at):
        self.game_end_at = game_end_at

    def set_game_password_collected(self, game_password_collected):
        self.game_password_collected = game_password_collected

    def set_game_completed_airports(self, game_completed_airports):
        self.game_completed_airports = game_completed_airports
