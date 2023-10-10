def calculate_maxdistance(user_money, user_fuel):
    max_distance = round(((user_money / 10 + user_fuel) * 10), 0)
    return max_distance
