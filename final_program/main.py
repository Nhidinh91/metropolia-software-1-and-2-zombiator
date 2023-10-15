import game_story as st
import get_dict_airportcoordinate_by_country as airport
import calculate_distance as cd
import get_dict_distance as dis
import calculate_maxdistance as mdis
import need_more_money as nm
import fuel_consume as fc
import convert_fuel_money as fm
import need_weapon_and_reward as wr
import list_airport as lp
import player as pl
import ranking as rk

# Define some global variables for the game
player_money = 500
player_fuel = 200
player_weapon = 200
final_weapon = 500
final_reward = 10000
current_location = "Finland"
final_location = "Spain"
dict_airport_coordinate = airport.get_dict_airportcoordinate_fromcountry()
condition_and_reward = wr.need_weapon_and_reward()

# Game starts
# Ask to show the story
read_story = input("Do you want to read the game story? (y/n):\n")
if read_story == "y":
    print(st.story)

player = input("Now you are ready to start!!!\nWhat's your name:\n")

# Check if the user exists in the database
if not pl.is_player_existed(player):
    # If the user doesn't exist, add them to the database
    pl.add_player(player, current_location)
    print(f"Hello {player}. ")
else:
    # If the user exists, print a welcome back message and set location to default
    pl.update_player(player[0], current_location)
    print(f"Welcome back, {player}. ")

# Get user info
player_info = pl.get_player_info(player)

print(f"\nThanks for joining the rescue team.\n Here is your first bag: {player_money} euros, {player_fuel} liters of fuel, and {player_weapon} weapons.")

# The game will run until the player_weapons are enough to do final
while player_weapon < final_weapon:
    max_distance = mdis.calculate_maxdistance(player_money, player_fuel)
    dict_distance = dis.get_dict_distance(current_location)

    # During the game, user can encounter the cases where user can move to any country
    # and player_weapon is too low to defeat the destination country
    # We have to give money and weapon
    if nm.need_more_money(max_distance, current_location) or player_weapon <= 50:
        print("You have too little money and weapons left.\nThe Red Cross Organization gives you 500 money, 100 liters of fuel and 150 weapons. Good luck")
        player_money += 500
        player_fuel += 100
        player_weapon += 200

    # The commands will be listed below
    print("\nChoose what you want to do now.\nInput 1 to choose the country you want to go.\nInput 2 to check your inventory and the approachable country list.\nInput 3 to buy more fuel.")

    command = input("You choose: \n")
    if command == "2":
        max_distance = mdis.calculate_maxdistance(player_money, player_fuel)
        dict_distance = dis.get_dict_distance(current_location)
        print(f"You have:\n{player_money} euros.\n{player_fuel} liters of fuel.\n{player_weapon} weapons")
        print("\nList of the approachable airports with your fuel and money at present:")
        lp.list_airport(max_distance, dict_distance)
    elif command == "3":
        while True:
            try:
                amount_fuel = float(input("It take 10 euros for 1 fuel. Please input the amount of fuel you want to buy:\n"))
                if amount_fuel > 0:
                    spent_money = fm.convert_fuel_money(amount_fuel)
                    if player_money >= spent_money:
                        player_money -= spent_money
                        player_fuel += amount_fuel
                        print(f"You have successfully purchased fuel. It took you {round(spent_money,0)} euros.\nNow you have {player_money} euros and {player_fuel} liters of fuel")
                        break
                    else:
                        print("You don't have enough money to buy this amount of fuel. Try again with a different quantity.\n")
                else:
                    print("The number is not valid. Please try again!\n")
            except:
                print("The number is not valid. Please try again!\n")
    elif command == "1":
        country_name = input("Please input the country you want to go:\n")
        if country_name not in dict_distance:
            print("Country not found. Please try another country in Schengen area")
        else:
            distance = cd.calculate_distance(current_location, country_name)
            need_fuel = fc.fuel_consumed(distance)
            if player_fuel >= need_fuel:
                current_location = country_name

                # Update new location
                pl.update_player(player, current_location)

                player_fuel -= need_fuel
                need_weapon = condition_and_reward[country_name][3]
                print(f"You have arrived in {country_name}.\nYou need {need_weapon} weapons to complete the mission here.\n")
                if player_weapon >= need_weapon:
                    player_weapon -= need_weapon
                    print(f"Congratulation! You have completed the mission to rescue {country_name}.")
                    rewards = condition_and_reward[country_name]
                    print(f"Here is your rewards for this mission:\n{rewards[1]} euros.\n{rewards[2]} weapons")
                    player_money += rewards[1]
                    player_weapon += rewards[2]
                    print(f"Now you have {player_money} euros and {player_weapon} weapons")
                else:
                    print(f"Unfortunately! You don't have enough weapons to complete the mission in {country_name}")
                    print("You got into trouble with zombies here and was rescued by the organization back to Helsinki, Finland.")
                    print("You have lost half of your money and weapons.\n")
                    player_money = round(0.5*player_money)
                    player_weapon = round(0.5*player_weapon)
                    current_location = "Finland"

                    # Update new location
                    pl.update_player(player, current_location)

                    print(f"Now you have {player_money} euros and {player_weapon} weapons.\n")
            else:
                print(f"You need to buy {(need_fuel)-(player_fuel)} liters of fuel to get there or choose another country.\n")
    else:
        print("Invalid command")

print(f"You have enough weapons to rescue people in the last country: {final_location}. Lets go to Madrid.")
print(f"It takes you {final_weapon} weapons to complete the final mission\n")
print(f"Congratulation! You have completed the final mission!\nYou got {final_reward} euros as a reward.\nNow you are the hero.\nLet's continue your next adventure: bring back the green planet. \nSee you in the next stage!")

# Update new location
pl.update_player(player[0], final_location)
distance = cd.calculate_distance(current_location, final_location)
# Calculate score
need_fuel = fc.fuel_consumed(distance)
player_money += final_reward
player_fuel -= need_fuel
player_weapon -= final_weapon
score = player_money + player_fuel*10 + player_weapon*10

# Get ranking info
ranking_info = rk.get_ranking_info(player_info[0])

# If there is no previous ranking info
# then add a new one, otherwise update it
if ranking_info is None:
    rk.add_ranking(player_info[0], score)
else:
    rk.update_player_score(player_info[0], score)

print(f"The game ends! You got {score} points totally.\n")

check_ranking = input("Would you like to see your rankings?(y/n)\n")
if check_ranking == "y":
    all_rankings = rk.get_all_player_ranking()
    for index, ranking in enumerate(all_rankings, start=1):
        if ranking[0] == player_info[0]:
            print(f"{index}/ \033[1m{ranking[1]} {ranking[2]}\033[0m <-----Here is your ranking")
        else:
            print(f"{index}/ {ranking[1]} {ranking[2]}")
