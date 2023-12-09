import os
import random
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_user, current_user

from app import db
from app.models.airport import Airport
from app.models.player import Player
from app.models.ranking import Ranking
from app.models.reward import Reward

from app.util.util import Util

from geopy.distance import geodesic

load_dotenv()

game = Blueprint("game", __name__)


@game.route("/game")
def home():
    # If the user is not logged in, redirect to the login page
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    return render_template("game/index.html", google_maps_api_key=google_maps_api_key)


@game.route("/game/airports", methods=["GET"])
def airports():
    airports = Airport.query.all()
    player = Player.query.filter_by(id=current_user.id).first()

    if not player:
        return jsonify({"status": -1, "message": "Cannot find player"})

    password_pieces = player.game_master_password.split(",")
    random.shuffle(airports)
    # Construct the airport list with password pieces
    # and weather information and rewards
    airport_list = []
    count = 0
    for airport in airports:
        # Ignore Spain and Finland airport

        if airport.country == "Spain":
            continue

        if airport.country == "Finland":
            password_piece = ""

        if count < 5:
            password_piece = password_pieces[count]
        elif count >= 5:
            password_piece = ""

        airport_info = {
            "id": airport.id,
            "ident": airport.ident,
            "name": airport.name,
            "password_piece": password_piece,
            "latitude_deg": airport.latitude_deg,
            "longitude_deg": airport.longitude_deg,
            "continent": airport.continent,
            "country": airport.country,
            "stage": airport.stage,
        }

        airport_list.append(airport_info)
        count += 1

    for airport in airport_list:
        latitude, longitude = str(airport["latitude_deg"]), str(
            airport["longitude_deg"]
        )

        # Get the weather information
        weather_info = Util.get_weather_info(latitude, longitude)
        point = weather_info["weather_point"]
        airport["temperature"] = weather_info["temperature"]
        airport["wind_speed"] = weather_info["wind_speed"]

        # Get the pollution information
        polution_info = Util.get_pollution_info(latitude, longitude)
        point += polution_info["pollution_point"]
        airport["pollution_level"] = polution_info["pollution_level"]

        # Get the rewards information
        rewards = Reward.query.all()
        reward_list = [
            {
                "name": reward.name,
                "amount": reward.amount,
                "difficult_level": reward.difficult_level,
                "passing_condition": reward.passing_condition,
            }
            for reward in rewards
        ]

        # Assign the rewards based on the difficulty level
        Util.update_airport_difficulty(airport, point, reward_list)

    # Call DB get Spain airport
    spain_airport = Airport.query.filter_by(country="Spain").first()
    spain_airport_dict = {
        "id": spain_airport.id,
        "ident": spain_airport.ident,
        "name": spain_airport.name,
        "latitude_deg": spain_airport.latitude_deg,
        "longitude_deg": spain_airport.longitude_deg,
        "continent": spain_airport.continent,
        "country": spain_airport.country,
        "stage": spain_airport.stage,
        "needed_weapon": 2000,
        "difficulty_level": "super_hard",
        "rewards_energy": 2000,
        "rewards_weapon": 2000,
        "password_piece": "",
    }

    airport_list.append(spain_airport_dict)

    return jsonify(
        {
            "status": 1,
            "message": "Airports fetched successfully",
            "airports": airport_list,
        }
    )


@game.route("/game/set-up", methods=["POST"])
def setup():
    player = Player.query.filter_by(id=current_user.id).first()
    if not player:
        return jsonify({"status": -1, "message": "No player found"})

    # The game hasn't started and need to be setup
    if player.game_status == "not_started":
        player.location = "Finland"
        player.inventory_weapon = os.getenv("INIT_WEAPONS_NUMBER")
        player.inventory_energy = os.getenv("INIT_ENERGY_NUMBER")
        player.game_start_at = None
        player.game_end_at = None
        player.game_actual_end_at = None
        player.game_paused_at = None
        player.game_password_collected = ""
        player.game_completed_airports = "Finland"
        player.game_master_password = ",".join(
            map(str, sorted(random.sample(range(10), 5)))
        )
        player.game_master_password_retry_times = 0

        login_user(player, remember=True, duration=timedelta(days=1))

        db.session.commit()

        return jsonify(
            {
                "status": 1,
                "message": "Game setup successfully",
                "player": player.get_info(),
            }
        )

    return jsonify({"status": 0, "message": "Game already setup"})


@game.route("/game/start", methods=["POST"])
def start():
    player = Player.query.filter_by(id=current_user.id).first()
    if not player:
        return jsonify({"status": -1, "message": "No player found"})

    # The game has already started
    if player.game_status == "started":
        player_info = player.get_info()
        player_info["game_start_at"] = player.game_start_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        player_info["game_end_at"] = player.game_end_at.strftime("%Y-%m-%d %H:%M:%S")

        return jsonify(
            {
                "status": 0,
                "message": "Game already started",
                "player": player_info,
            }
        )

    # The game is paused
    if player.game_status == "paused":
        player_info = player.get_info()

        used_time = player_info["game_paused_at"] - player_info["game_start_at"]
        total_time = player_info["game_end_at"] - player_info["game_start_at"]

        player_info["game_start_at"] = datetime.now()
        player_info["game_end_at"] = player_info["game_start_at"] + (
            total_time - used_time
        )
        player_info["game_start_at"] = player_info["game_start_at"].strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        player_info["game_end_at"] = player_info["game_end_at"].strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        player_info["game_paused_at"] = player.game_paused_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        return jsonify(
            {
                "status": 0,
                "message": "Game is paused",
                "player": player_info,
            }
        )

    # Game in the stage where the player has reached the final airport and need to enter the master password
    if player.game_status == "need_master_password":
        player_info = player.get_info()
        player_info["game_start_at"] = player.game_start_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        player_info["game_end_at"] = player.game_end_at.strftime("%Y-%m-%d %H:%M:%S")

        return jsonify(
            {
                "status": 0,
                "message": "Game in the nearlly finished",
                "player": player_info,
            }
        )

    # Game already finished and the game result is success
    if player.game_status == "completed":
        player_info = player.get_info()
        player_info["game_start_at"] = player.game_start_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        player_info["game_end_at"] = player.game_end_at.strftime("%Y-%m-%d %H:%M:%S")

        return jsonify(
            {
                "status": 0,
                "message": "Game already finished successfully",
                "player": player_info,
            }
        )

    # Game already finished and the game result is failure
    if player.game_status == "failed":
        player_info = player.get_info()
        player_info["game_start_at"] = player.game_start_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        player_info["game_end_at"] = player.game_end_at.strftime("%Y-%m-%d %H:%M:%S")

        return jsonify(
            {
                "status": 0,
                "message": "Game already finished, but failed",
                "player": player_info,
            }
        )

    player.game_status = "started"
    player.game_start_at = datetime.now()
    player.game_end_at = datetime.now() + timedelta(minutes=10)

    db.session.commit()

    login_user(player, remember=True, duration=timedelta(days=1))

    player_info = player.get_info()
    player_info["game_start_at"] = player.game_start_at.strftime("%Y-%m-%d %H:%M:%S")
    player_info["game_end_at"] = player.game_end_at.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(
        {"status": 1, "message": "Game started successfully", "player": player_info}
    )


@game.route("/game/rescue-airport", methods=["POST"])
def rescue_airport():
    # Get the player from the db
    player = Player.query.filter_by(id=current_user.id).first()

    # Some validation
    if not player:
        return jsonify({"status": -1, "message": "No player found with this email"})

    if player.game_status == "not_started":
        return jsonify({"status": -1, "message": "Game not started"})

    if player.game_status == "completed" or player.game_status == "failed":
        return jsonify({"status": -1, "message": "Game already finished"})

    rescue_status = request.json["rescue_status"]
    # If the airport is rescued successfully, then update the player info
    if int(rescue_status) == 1:
        # Get the player info from the request
        location = request.json["new_location"]
        inventory_weapon = request.json["inventory_weapon"]
        inventory_energy = request.json["inventory_energy"]
        game_completed_airports = request.json["completed_airports"]
        game_password_collected = request.json["password_collected"]
        airport_stage = request.json["airport_stage"]

        # Update the player info
        player.location = location
        player.inventory_weapon = inventory_weapon
        player.inventory_energy = inventory_energy
        player.game_completed_airports = ",".join(
            list(dict.fromkeys(game_completed_airports.split(",")))
        )
        # If the player hasn't collected all the password pieces, sort them in the correct order and save them
        if len(player.game_password_collected.split(",")) < 5:
            game_password_collected = list(
                dict.fromkeys(game_password_collected.split(","))
            )
            player.game_password_collected = ",".join(
                map(str, sorted(game_password_collected))
            )

        # If final airport is reached, then game_status = 2,
        # meaning the player needs to enter the master password
        if int(airport_stage) == 2 and location == "Spain":
            player.game_status = "need_master_password"
    else:
        # If the airport is not rescued successfully, then update the player info
        inventory_weapon = request.json["inventory_weapon"]
        inventory_energy = request.json["inventory_energy"]

        player.inventory_weapon = inventory_weapon
        player.inventory_energy = inventory_energy

    db.session.commit()

    login_user(player, remember=True, duration=timedelta(days=1))

    return jsonify(
        {
            "status": 1,
            "message": "Player info updated successfully",
            "player": player.get_info(),
        }
    )


@game.route("/game/end", methods=["POST"])
def end():
    player = Player.query.filter_by(id=current_user.id).first()
    if not player:
        return jsonify({"status": -1, "message": "No player found with this email"})

    if player.game_status == "not_started":
        return jsonify({"status": -1, "message": "Game not started"})

    if player.game_status == "completed" or player.game_status == "failed":
        return jsonify({"status": -1, "message": "Game already finished"})

    game_status = request.json["game_status"]

    player.game_status = game_status
    player.game_actual_end_at = datetime.now()
    db.session.commit()

    login_user(player, remember=True, duration=timedelta(days=1))

    # Only update or add the ranking if the game is finished successfully
    if game_status == "completed":
        # Calculate the game duration
        game_duration = player.game_actual_end_at - player.game_start_at
        # Calculate the time remaining
        time_remaining = player.game_end_at - player.game_actual_end_at

        # Get these values from the db
        weapons_remaining = player.inventory_weapon
        energy_remaining = player.inventory_energy

        calculated_score = Util.calculate_score(
            weapons_remaining, energy_remaining, time_remaining.total_seconds()
        )

        # add or update the ranking
        ranking_exists = Ranking.query.filter_by(player_id=player.id).first()
        if ranking_exists:
            ranking_exists.score = round(calculated_score)
            ranking_exists.duration = game_duration.total_seconds()
            ranking_exists.weapon_remaining = weapons_remaining
            ranking_exists.energy_remaining = energy_remaining

            db.session.add(ranking_exists)
            db.session.commit()
        else:
            ranking = Ranking(
                player_id=player.id,
                score=round(calculated_score),
                duration=game_duration.total_seconds(),
                weapon_remaining=weapons_remaining,
                energy_remaining=energy_remaining,
            )
            db.session.add(ranking)
            db.session.commit()

    return jsonify(
        {
            "status": 1,
            "message": "Game finished successfully",
            "player": player.get_info(),
        }
    )


@game.route("/game/result", methods=["GET"])
def result():
    player = Player.query.filter_by(id=current_user.id).first()
    if not player:
        return jsonify({"status": -1, "message": "No player found with this email"})

    if player.game_status == "not_started":
        return jsonify({"status": -1, "message": "Game not started"})

    if player.game_status == "started" or player.game_status == "need_master_password":
        return jsonify({"status": -1, "message": "Game not finished"})

    # Calculate the game duration
    game_duration = player.game_actual_end_at - player.game_start_at
    # Calculate the time remaining
    time_remaining = player.game_end_at - player.game_actual_end_at

    # Get these values from the db
    weapons_remaining = player.inventory_weapon
    energy_remaining = player.inventory_energy

    calculated_score = Util.calculate_score(
        weapons_remaining, energy_remaining, time_remaining.total_seconds()
    )

    return jsonify(
        {
            "status": 1,
            "message": "Game result fetched successfully",
            "player": player.get_info(),
            "game_status": player.game_status,
            "calculated_score": round(calculated_score),
            "game_duration": game_duration.total_seconds(),
            "weapons_remaining": weapons_remaining,
            "energy_remaining": energy_remaining,
        }
    )


@game.route("/game/retry", methods=["GET"])
def retry():
    player = Player.query.filter_by(id=current_user.id).first()
    if not player:
        return jsonify({"status": -1, "message": "No player found with this email"})

    if player.game_status == "not_started":
        return jsonify({"status": -1, "message": "Game not started"})

    # Reset the player info to the initial state
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

    login_user(player, remember=True, duration=timedelta(days=1))

    return jsonify(
        {
            "status": 1,
            "message": "Game retry successful",
            "player": player.get_info(),
        }
    )


@game.route("/game/unclock-master-password", methods=["POST"])
def unclock_master_password():
    # Get the player info from the request
    master_password = request.json["master_password"]

    # Get the player from the db
    player = Player.query.filter_by(id=current_user.id).first()

    # Some validation
    if not player:
        return jsonify({"status": -1, "message": "No player found with this email"})

    if player.game_status == "not_started":
        return jsonify({"status": -1, "message": "Game not started"})

    if player.game_status == "completed" or player.game_status == "failed":
        return jsonify({"status": -1, "message": "Game already finished"})

    # Check if the master password is correct
    if (
        player.game_master_password == master_password
        and player.game_master_password_retry_times < 5
    ):
        return jsonify(
            {
                "status": 1,
                "message": "Master password correct",
                "player": player.get_info(),
            }
        )
    elif (
        player.game_master_password_retry_times > 5
    ):  # If the player has tried more than 5 times, then game_status = 4 meaning the game is failed
        player.game_status = "failed"
        player.game_actual_end_at = datetime.now()
        db.session.commit()

        login_user(player, remember=True, duration=timedelta(days=1))

        return jsonify(
            {
                "status": -1,
                "message": "Master password incorrect, and you have tried more than 5 times",
                "player": player.get_info(),
            }
        )
    else:
        player.game_master_password_retry_times += 1
        db.session.commit()

        login_user(player, remember=True, duration=timedelta(days=1))

        message = "Master password incorrect. You have " + str(
            5 - player.game_master_password_retry_times
        ) + " times left"

        if player.game_master_password_retry_times == 5:
            message = (
                "Master password incorrect. You have tried more than 5 times, and the game is failed"
            )
        
        return jsonify(
            {
                "status": -1,
                "message": message,
                "player": player.get_info(),
            }
        )


@game.route("/game/rankings", methods=["GET"])
def rankings():
    rankings = Ranking.query.order_by(Ranking.score.desc()).limit(5).all()
    ranking_list = [ranking.get_info() for ranking in rankings]
    # Get the player info from the list
    for ranking in ranking_list:
        player = Player.query.filter_by(id=ranking["player_id"]).first()
        ranking["player_name"] = player.name
        ranking["player_position"] = ranking_list.index(ranking) + 1

    # Get current player's ranking
    player = Player.query.filter_by(id=current_user.id).first()
    player_ranking = Ranking.query.filter_by(player_id=player.id).first()
    player_ranking_info = player_ranking.get_info()
    player_ranking_info["player_name"] = player.name

    # If player is not in the top 5, then add the player to the list only 1 time
    is_player_in_ranking = False
    for ranking in ranking_list:
        if ranking["player_id"] == player_ranking_info["player_id"]:
            is_player_in_ranking = True
            break

    if not is_player_in_ranking:
        player_ranking_info["player_name"] = player.name
        # Get the player position is equal to the position in the database + 1
        # Get all the rankings from the database
        all_rankings = Ranking.query.order_by(Ranking.score.desc()).all()
        # Get the player position
        player_ranking_info["player_position"] = all_rankings.index(player_ranking) + 1

        return jsonify(
            {
                "status": 1,
                "message": "Rankings fetched successfully",
                "rankings": ranking_list,
                "player_ranking": player_ranking_info,
            }
        )

    return jsonify(
        {
            "status": 1,
            "message": "Rankings fetched successfully",
            "rankings": ranking_list,
        }
    )


@game.route("/game/update-player-info", methods=["POST"])
def update_player_info():
    # Get the player info from the request
    name = request.json["player_name"]

    # Get the player from the db
    player = Player.query.filter_by(id=current_user.id).first()

    # Some validation
    if not player:
        return jsonify({"status": -1, "message": "No player found with this email"})

    # Update the player info
    player.name = name

    db.session.commit()

    login_user(player, remember=True, duration=timedelta(days=1))

    return jsonify(
        {
            "status": 1,
            "message": "Player info updated successfully",
            "player": player.get_info(),
        }
    )


@game.route("/game/pause-or-resume-game-timer", methods=["POST"])
def pause_or_resume_game_timer():
    # Get the player info from the request
    pause_or_resume = request.json["pause_or_resume"]

    # Get the player from the db
    player = Player.query.filter_by(id=current_user.id).first()

    # Some validation
    if not player:
        return jsonify({"status": -1, "message": "No player found with this email"})

    # Update the player info
    if pause_or_resume == "pause":
        player.game_paused_at = datetime.now()
        player.game_status = "paused"
    elif pause_or_resume == "resume":
        used_time = player.game_paused_at - player.game_start_at
        total_time = player.game_end_at - player.game_start_at
        player.game_start_at = datetime.now()
        player.game_end_at = player.game_start_at + (total_time - used_time)
        player.game_paused_at = None
        player.game_status = "started"

    db.session.commit()

    login_user(player, remember=True, duration=timedelta(days=1))

    player_info = player.get_info()
    player_info["game_end_at"] = player.game_end_at.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(
        {
            "status": 1,
            "message": "Game timer updated successfully",
            "player": player_info,
        }
    )


@game.route(
    "/game/check-needed-energy/<current_location>/<destination>/", methods=["GET"]
)
def check_energy_of_two_location(current_location, destination):
    if current_user.game_status == "not_started":
        return jsonify({"status": -1, "message": "Game not started"})

    if current_user.game_status == "completed" or current_user.game_status == "failed":
        return jsonify({"status": -1, "message": "Game already finished"})

    if current_user.game_status == "need_master_password":
        return jsonify(
            {
                "status": -1,
                "message": "You are defeated the boss stage, please enter the master password",
            }
        )

    if current_location == destination:
        return jsonify(
            {
                "status": -1,
                "message": "The two locations are the same, no energy needed",
            }
        )

    if current_location == "" or destination == "":
        return jsonify({"status": -1, "message": "The two locations are not valid"})

    # Get the airport from the db
    current_location_info = Airport.query.filter_by(country=current_location).first()
    current_coordinate = (
        current_location_info.latitude_deg,
        current_location_info.longitude_deg,
    )
    destination_info = Airport.query.filter_by(country=destination).first()
    destination_coordinate = (
        destination_info.latitude_deg,
        destination_info.longitude_deg,
    )
    distance = round(geodesic(current_coordinate, destination_coordinate).kilometers, 0)
    needed_energy = distance

    return jsonify(
        {
            "status": 1,
            "message": "Game timer updated successfully",
            "needed_energy": needed_energy,
        }
    )
