import mysql.connector

connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        database="zombiator",
        user="root",
        password="Bu@1234#Li",
        autocommit=True
    )

def get_dict_airportcoordinate_by_country():
    dict_airport_coordinate = {}
    sql = "SELECT country, latitude_deg, longitude_deg FROM airport"

    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            coordinate = (row[1], row[2])
            dict_airport_coordinate[row[0]] = coordinate
    return dict_airport_coordinate

import get_dict_distance as dis
import random
import dbconnection as db

condition_and_reward = {}
difficult = ["easy", "normal", "hard"]


def need_weapon_and_reward():
    list_country = dis.get_dict_distance("Finland")
    count = 0
    for country in list_country:
        if count == 4 and "hard" in difficult:
            difficult.remove("hard")
        difficult_level = random.choice(difficult)
        if difficult_level == "hard":
            count += 1
        sql = "SELECT name, min_amount, max_amount, difficult_level, passing_condition FROM reward"
        reward = []
        cursor = db.db_connection()
        cursor.execute(sql)
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            reward.append(difficult_level)
            for row in result:
                if row[3] == difficult_level:

                    if row[0] == "money" or row[0] == "weapon":
                        reward.append(random.randint(row[1], row[2]))
                        reward.append(row[4])
            reward.pop(2)
            condition_and_reward[country] = reward
    return condition_and_reward
def calculate_maxdistance(user_money,user_fuel):
    money_to_fuel = user_money / 10
    fuelmax = money_to_fuel + user_fuel
    max_distance = fuelmax * 10
    return max_distance

def need_more_money(max_distance,current_location):
    dict_distance = get_dict_distance(current_location)
    list_distance = []
    for country in dict_distance:
        if dict_distance[country] != 0:
          list_distance.append(dict_distance[country])
    return max_distance < min(list_distance)

user_money = 500
user_fuel = 150
user_weapon = 200
final_weapon = 2000
final_reward = 10000
current_location = "Finland"

name = input("Please enter your name:")
print(f"Welcome to Zombiator,{name}!\nYou are going to save the world!\nNow start!")

while user_weapon < final_weapon:
    max_distance = calculate_maxdistance(user_money,user_fuel)
    dict_distance = get_dict_distance(current_location)
    if (need_more_money(max_distance,current_location) or user_weapon) <= 50:
        user_money = user_money + 50
        user_weapon = user_weapon + 150