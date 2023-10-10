def calculate_maxdistance(player_money, player_fuel):
    max_distance = round(((player_money / 10 + player_fuel) * 10), 0)
    return max_distance
