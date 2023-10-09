
command = 1

if command == 1:
    country_name = input("Enter country name: ")
    distance = calculate_distance(current_location, country_name)
    need_fuel = fuel_consumed(distance)
    if user_fuel >= need_fuel:
        current_location = country_name
        user_fuel -= need_fuel
        print(f"You have arrived in {current_location}. Fuel remaining: {user_fuel:.2f} liters.")
    else:
        print("You don't have enough fuel to reach the destination!")