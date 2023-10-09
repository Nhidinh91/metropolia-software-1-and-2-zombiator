print(f"You have enough weapons to rescue people in the last country: {final_location}. Lets go to Madrid.\n")
print(f"It takes you {final_weapon} weapons to complete the final mission")
print(f"Bravo! You have completed the final mission!\nYou got {final_reward} euros as a reward.\n")

# Update new location
pl.update_player(player, final_location)

# Calculate score
distance = cd.calculate_distance(current_location, final_location)
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
        if ranking[0] == player:
            print(f"{index}/ \033[1m{ranking[0]} {ranking[1]}\033[0m <-----Here is your ranking")
        else:
            print(f"{index}/ {ranking[0]} {ranking[1]}")