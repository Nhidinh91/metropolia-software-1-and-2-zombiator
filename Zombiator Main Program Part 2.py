# For Project Software 1 13/10/2023

# BB's Part codes

# Main program part 2

def list_airport(max_distance, dict_distance):
    for country in dict_distance:
        if 0 < dict_distance[country] <= max_distance:
            print(f"{country} {dict_distance[country]} km")

command = input("Choose option: \n")
if command == "2":
    # Assume maximum distance (from def calculate_maxdistance(player_money, player_fuel) function)
    max_distance = float(input("Enter the maximum distance: "))
    # Assume distance from other countries
    dict_distance = {"Country1": 120.45, "Country2": 8397.43, "Country3": 12345, "Country4": 24.5}
    player_money = 3349  # Assume the player's money remaining
    player_fuel = 70  # Assume the player's fuel remaining
    player_weapon = 534  # Assume the player's weapons remaining
    # Display player's profile
    print(f"You have:\n{player_money} euros.\n{player_fuel} liters of fuel.\n{player_weapon} weapons")
    print("\nList of airports currently accessible with your fuel and money at present:")
    list_airport(max_distance, dict_distance)


