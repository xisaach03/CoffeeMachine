# ============================================================
#  Project: Coffee Machine Simulation
#  File: main.py
#
#  Author(s): Sofia Vanessa and Ximena Isaac
#
#  Credits:
#    - Functional design and logic implemented by both authors.
#    - Output formatting (pretty menus, emoji styling) by Sofia Vanessa.
#
#  Notes:
#    This project was created for learning purposes. 
# ============================================================


from coffeeprep import Coffee, StockIngredients

# ------------------------------------------------------------------------------------------------------------------------------- #
#                                                         Menu User Selection                                                     #
# ------------------------------------------------------------------------------------------------------------------------------- #

'''
aquí pon la implementación del menu

def display_menu():
puedes poner un menu bonito con las opciones de café

def get_coffee_selection(): espresso, latte, capuccino

def get_size(): small, medium, large
'''
def display_main_menu():
    print("\n" + "="*50)
    print("WELCOME TO THE COFFEE MACHINE ")
    print("="*50)
    print("1.-Order Coffee")
    print("2.-Fill the Machine")
    print("3.-Withdraw Money")
    print("4.-Check Status")
    print("5.-Exit")
    print("="*50)

def display_menu():
    print("\nSelect the type of coffee:")
    print("1. Espresso")
    print("2. Latte")
    print("3. Capuccino")

def get_coffee_selection():
    choice = input("Enter your choice (1, 2, 3): ")
    return {"1": "espresso", "2": "latte", "3": "capuccino"}.get(choice, "espresso")

def get_size():
    return input("Enter size (small, medium, large): ").lower()

def refill_water(stock):
    current = stock.stock["water"]
    max_capacity = 2000
    if current == 2000:
        print("Water tank is already full.")
    else:
        refill_amount = max_capacity - current
        stock.stock["water"] += refill_amount
        print(f"Refilled water by {refill_amount}ml.")

def refill_milk(stock):
    current = stock.stock["milk"]
    max_capacity = 1000
    if current == max_capacity:
        print("Milk tank is already full.")
    else:
        refill_amount = max_capacity - current
        stock.stock["milk"] += refill_amount
        print(f"Refilled milk by {refill_amount}ml.")

def refill_coffee_beans(stock):
    current = stock.stock["coffee_beans"]
    max_capacity = 500
    if current == max_capacity:
        print("Coffee beans tank is already full.")
    else:
        refill_amount = max_capacity - current
        stock.stock["coffee_beans"] += refill_amount
        print(f"Refilled coffee beans by {refill_amount}g.")

def fill_all(stock):
    refill_water(stock)
    refill_milk(stock)
    refill_coffee_beans(stock)

def fill_machine(stock):
    # Function to fill the machine with ingredients
    print("Current stock:", stock.stock)
    print("\nWhat would you like to refill?")
    print("1.-Water 2.-Milk 3.-Coffe Beans 4.-Fill All")
    choice = input("Enter your choice (1-4): ")
    if choice == "1":
        refill_water(stock)
        print("Water refill complete.", stock.stock)
    elif choice == "2":
        refill_milk(stock)
        print("Milk refill complete.", stock.stock)
    elif choice == "3":
        refill_coffee_beans(stock)
        print("Coffee beans refill complete.", stock.stock)
    elif choice == "4":
        fill_all(stock)
        print("All ingredients refill complete.", stock.stock)
    else:
        print("Invalid choice.")
        fill_machine(stock)



# ------------------------------------------------------------------------------------------------------------------------------- #
#                                          Simulation of the coffee machine interaction                                           #
# ------------------------------------------------------------------------------------------------------------------------------- #

def main():
    money = 0
    stock = StockIngredients()                                           # representing the stock of the coffee machine
    print("Initial stock:", stock.stock)                                 # Display initial stock

    while True:
        display_main_menu()
        main_choice = input("Select option(1-5): ")
        if main_choice == "1":
            display_menu()
            coffee_type = get_coffee_selection()
            size = get_size()

            coffee = Coffee(coffee_type, size)                                 # Create the coffee object based on user selection
            print(f"\nYou selected a {size} {coffee_type}.")

            ingredients_needed = coffee.ingredients                          # Check if ingredients are available for the selected coffee
            available, output = stock.check_ingredients(ingredients_needed)
            print(output)

            if available:                                                    # HAPPY PATH - Ingredients available
                print(f"\nPreparing your {size} {coffee_type}...")
                stock.take_ingredients(ingredients_needed)                   # Reduce the stock based on selected coffee ingredients
                print(f"Your {size} {coffee_type} is ready!")
                print("Updated stock:", stock.stock)

            #another_coffee = input("Do you want to make another coffee? (yes/no): ").lower()
            #if another_coffee == "no":
            #    print("Thank you for using the coffee machine!")
               # break
            
        elif main_choice == "2":                                             # Refill ingredients on stock
            fill_machine(stock)

if __name__ == "__main__":
    main()
