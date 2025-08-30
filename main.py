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

# ------------------------------------------------------------------------------------------------------------------------------- #
#                                          Simulation of the coffee machine interaction                                           #
# ------------------------------------------------------------------------------------------------------------------------------- #

def main():

    stock = StockIngredients()                                           # representing the stock of the coffee machine
    print("Initial stock:", stock.stock)                                 # Display initial stock

    while True: 
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

        another_coffee = input("Do you want to make another coffee? (yes/no): ").lower()
        if another_coffee == "no":
            print("Thank you for using the coffee machine!")
            break

if __name__ == "__main__":
    main()
