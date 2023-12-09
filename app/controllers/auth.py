from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app.models.player import Player
from app import db
from datetime import timedelta
import os
from dotenv import load_dotenv

auth = Blueprint("auth", __name__)

load_dotenv()

@auth.route("/")
def login():
    # If the user is already logged in, redirect to the game page
    if current_user.is_authenticated:
        return redirect(url_for("game.home"))

    return render_template("auth/login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.json["email"]
    password = request.json["password"]

    player = Player.query.filter_by(email=email).first()

    if not player:
        # User does not exist, create a new user
        new_player = Player(email=email, name=email.split("@")[0], password=password)
        db.session.add(new_player)
        db.session.commit()

        # Log in the new user with duration is 1 day
        login_user(new_player, remember=True, duration=timedelta(days=1))

        return jsonify(
            {"status": 1, "message": "Player created and logged in successfully"}
        )
    else:
        # User exists, check the password
        if player.check_password(password):
            # Password is correct, log in the player
            login_user(player, remember=True, duration=timedelta(days=1))
            return jsonify({"status": 1, "message": "Logged in successfully"})
        else:
            # Password is incorrect
            return jsonify({"status": -1, "message": "Invalid credentials"})


@auth.route("/logout")
@login_required
def logout():
    player = Player.query.filter_by(id=current_user.id).first()
    player.game_status = "not_started"
    player.game_start_at = None
    player.game_end_at = None
    player.game_actual_end_at = None
    player.game_paused_at = None
    player.game_password_collected = ""
    player.game_completed_airports = "Finland"
    player.game_master_password = ""
    player.game_master_password_retry_times = 0
    player.inventory_weapon = os.getenv("INIT_WEAPONS_NUMBER")
    player.inventory_energy = os.getenv("INIT_ENERGY_NUMBER")
    player.location = "Finland"
    
    db.session.commit()

    logout_user()
    
    return jsonify({"status": 1, "message": "Logged out successfully"})
