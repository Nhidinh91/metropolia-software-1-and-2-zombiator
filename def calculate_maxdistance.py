def calculate_maxdistance(user_money,user_fuel):
    money_to_fuel = user_money / 10
    fuelmax = money_to_fuel + user_fuel
    max_distance = fuelmax * 10
    return max_distance