# For Project Software 1 13/10/2023

# BB's Part codes

# 7. convert_fuel_money(amount_fuel)
#1st idea (without loop)

# Define the function
def convert_fuel_money(amount_fuel):
    spent_money = amount_fuel * 10
    return spent_money

# To assume the amount of fuel you want to buy, I created an input.
try:
    amount_fuel = (float(input("Enter the amount of fuel you want to buy in liters: ")))
    spent_money = convert_fuel_money(amount_fuel)
    print(f"The money you have to spend is {spent_money:.2f} euros.")
# If it is not the number input...
except ValueError:
    print("Invalid input.")


# 2nd idea (with loop according to the flowchart)

# Define the function
def convert_fuel_money(amount_fuel, fuel_price=10):
    return amount_fuel * fuel_price

# To assume the current amount of money, I created an input.
current_money = (float(input("Enter your current amount of money: ")))

# Loop main program
while True:
    try:
        amount_fuel = (float(input("Enter the amount of fuel you want to buy in liters: ")))
        spent_money = convert_fuel_money(amount_fuel)
        # If your money amount is enough to buy fuel(s):
        if current_money >= spent_money:
            # Subtract the amount of money
            current_money -= spent_money
            print(f"The money you have to spend is {spent_money:.2f} euros.")
            print(f"The remaining amount of money is {current_money:.2f} euros.")
            break
        # If your money amount is not enough to buy fuel(s), the program will let you input (amount_fuel) again.
        else:
            print("Cannot purchase. Please enter less amount of fuel.")
    # If it is not the number input...
    except ValueError:
        print("Invalid input.")