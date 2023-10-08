# For Project Software 1 13/10/2023

# BB's Part codes

# 6. fuel_consumed(distance)
def fuel_consumed(distance):
    need_fuel = distance/10
    return need_fuel

# To assume the number of distance you've travelled and convert into fuel in liters, I created an input.
try:
    distance = (float(input("Enter the current distance you've travelled: ")))
    need_fuel = fuel_consumed(distance)
    print(f"The fuel you used was {need_fuel:.2f} liters.")
# If it is not the number input...
except ValueError:
    print("Invalid input.")