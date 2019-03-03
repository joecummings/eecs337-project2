class Recipe:
    def __init__(self, name):
        self.name = name
        self.number_of_reviews = 0
        self.rating = 0
        self.calories = 0
        self.ingredients = []
        self.tools = []
        self.methods = []
        self.steps = []

    def get_ingredients(self):
        return self.ingredients
    
    def get_tools(self):
        return self.tools
    
    def get_methods(self):
        return self.methods
    
    def get_steps(self):
        return self.steps

    def add_ingredient(self,ingredient):
        self.ingredients.append(ingredient)
        return
    
    def add_tool(self, tool):
        self.tools.append(tool)
        return

    def add_method(self,method):
        self.method.append(method)
        return

    def add_step(self,step):
        self.step.append(step)
        return

    def set_rating(self,rating):
        self.rating = rating
        return

    def set_number_of_reviews(self, reviews):
        self.number_of_reviews = reviews
        return
    
    def set_calories(self,calories):
        self.calories = calories
        return

class Ingredient:
    def __init__(self, name, quantity = 0,measurement = "", descriptor = "", preparation=""):
        self.name = name
        self.quantity = quantity
        self.measurement = measurement
        self.descriptor = descriptor
        self.preparation = preparation

def build_ingredient(str):
    return str