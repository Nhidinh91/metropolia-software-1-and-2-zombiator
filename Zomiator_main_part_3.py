user_money = 1000
user_fuel = 0

while True:
    command = input("Enter an option to continue or quite: ")

    if command == "3":
        while True:
            amount = int(input("Enter how much fuel do you want to buy: "))
            price_per_unit = 10  # Assuming the price per unit of fuel is $2
            spent_money = amount * price_per_unit

            if user_money >= spent_money:
               user_money -= spent_money
               user_fuel += amount
               print(f"You have purchased {amount}l of fuel.")
               print(f"Your remaining balance is {user_money} euros.")
               break
            else:
                print("Insufficient funds. Please enter a smaller quantity or quit.")
    else:
        break



