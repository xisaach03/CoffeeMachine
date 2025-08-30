# ============================================================
#  Project: Coffee Machine Simulation
#  File: coffeeprep.py
#
#  Author(s): Sofia Vanessa and Ximena Isaac
#
#  Credits:
#    - Functional design and logic implemented by both authors.
#
#  Notes:
#    This project was created for learning purposes. 
# ============================================================

SIZE_INCREMENT = {
    "small": 1.0,                                                   # Base size (no increment)
    "medium": 1.2,                                                  # 20% more ingredients and price
    "large": 1.5,                                                   # 50% more ingredients and price
}

#This class stores the amount of ingredients the machine has
class StockIngredients:                                         
    def __init__(self):
        self.stock = {                                              # Data structure (dictionary)
            "water": 2000,                                          # Unit: mililiters
            "milk": 1000,                                           # Unit: mililiters
            "coffee_beans": 500,                                    # Unit: grams
        }

    def check_ingredients(self, ingredients_needed):
        for ingredient, amount in ingredients_needed.items():
            if self.stock.get(ingredient, 0) < amount:              # Control structure
                return False, f"There's not enough {ingredient} in the machine, try another coffee"
        return True, "Ingredients available"
    
    def take_ingredients(self, ingredients_needed):
        for ingredient, amount in ingredients_needed.items():
            if ingredient in self.stock:
                self.stock[ingredient] -= amount                    # Operators used

    def add_ingredients(self, ingredient, amount):
        if ingredient in self.stock:
            self.stock[ingredient] += amount
        else:
            self.stock[ingredient] = amount
        print(f"{ingredient} re-filled with {amount} units")

#This class stores the properties of the coffee
class Coffee:
    def __init__(self, type, size, ingredients=None):
        self.type = type
        self.size = size
        self.ingredients = ingredients if ingredients else self.default_ingredients()  
        self.price = self.calculate_price()

    '''
    The base_ingredients dictionary defines the default ingredient amounts 
    (water, milk, and coffee beans, price) for each coffee type. These values 
    represent the recipe for the "small" size. If a larger size is chosen, 
    the ingredient amounts and price are scaled proportionally by 20% or 50%.
    '''
    def default_ingredients(self):
        base_ingredients = {
            "espresso": {"water": 250, "milk": 0, "coffee_beans": 16, "price": 4},
            "latte": {"water": 350, "milk": 75, "coffee_beans": 20}, "price": 7,
            "capuccino": {"water": 200, "milk": 100, "coffee_beans": 12, "price": 6}
        }
        
        recipe = base_ingredients.get(self.type)
        if not recipe:
            raise ValueError(f"Type of coffee '{self.type}' not found.")
        
        self.base_price = recipe["price"]
        recipe = {k: v for k, v in recipe.items()                  # Reconstruction of the dictionary by  key-value iteration 
                  if k != "price"}                                 # Removed "price"
        return self.adjust_ingredients_size(recipe)

    def adjust_ingredients_size(self, base_ingredients):
        multiplier = SIZE_INCREMENT.get(self.size, 1.0)             # Used SIZE_INCREMENT declared at the top
        adjusted_ingredients = {ingredient: amount * multiplier for ingredient, amount in base_ingredients.items()}
        return adjusted_ingredients
    
    def calculate_price(self):
        factor = SIZE_INCREMENT.get(self.size, 1.0)
        return round(self.base_price * factor, 2)

    def display_coffee_info(self):
        return f"Café: {self.type} | Tamaño: {self.size} | Precio: {self.price} u | Ingredientes: {self.ingredients}"