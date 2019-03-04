from nltk import MWETokenizer
import json
import re
import string
import scraper as s
ingredients = set([])
tokenizer = MWETokenizer()
measurements = set([])
techniques = set([])



def pull_nyt(recipes):
    res = s.pull_ingredients(recipes)
    return res
    
def load_ingredients():
    with open("ingredients.json") as file:
        data = json.load(file)
        print("\nBuilding Multi Word Tokenizer...")
        for i in data:
            for ingredient in i['ingredients']:
                s = ingredient.split()
                res = "_".join(s)
                ingredients.add(res)
                tokenizer.add_mwe(s)
    print("Ingredients Loaded: {0}\n".format(len(ingredients)))

def load_corpus():
    with open("corpus.json") as file:
        data = json.load(file)
        print("\nBuilding Measurement and Preparation Tokens...")
        for i in data['measurements']:
            measurements.add(i)
        for j in data['techniques']:
            techniques.add(j)

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

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
        return

    def add_tool(self, tool):
        self.tools.append(tool)
        return

    def add_method(self, method):
        self.methods.append(method)
        return

    def add_step(self, step):
        self.steps.append(step)
        return

    def set_rating(self, rating):
        self.rating = rating
        return

    def set_number_of_reviews(self, reviews):
        self.number_of_reviews = reviews
        return

    def set_calories(self, calories):
        self.calories = calories
        return


class Ingredient:
    def __init__(self, name, quantity=0, measurement="", descriptor="", preparation=""):
        self.name = name
        self.quantity = quantity
        self.measurement = measurement
        self.conversion = "N/A"
        self.descriptor = descriptor
        self.preparation = preparation


def build_ingredient(s):
    match = re.search(r'\((.*?)\)', s)
    if match is not None:
        alternate_measurement = match.groups()[0]
        s = s.replace("(" + alternate_measurement + ")", "")
    else:
        alternate_measurement = "N/A"
    if ", " in s:
        prep = s.split(", ")
        preparation = prep[1]
        phrase = prep[0]
    else:
        phrase = s
        preparation = "N/A"
    words = tokenizer.tokenize(phrase.split())
    name = tag_ingredient_name(words)
    quantity = tag_ingredient_quantity(words, name)
    sent = " ".join(words)
    sent = sent.replace(quantity, "")
    sent = sent.replace(name, "")
    words = sent.split()
    measurement = tag_ingredient_measurement(words)
    sent = " ".join(words)
    sent = sent.replace(measurement, "")
    
    print("Ingredient: {0} -- Quantity: {1} -- Measurement-- {2} -- Preparation: {3} -- Descriptors: {4}".format(
        name, quantity, measurement, preparation, sent))
    return s

def tag_ingredient_measurement(words):
    measure = "N/A"
    for word in words:
        if word in measurements:
            measure = word
    return measure
    

def tag_ingredient_name(words):
    name = "N/A"
    for word in words:
        if word in ingredients:
            name = word
    return name


def tag_ingredient_quantity(words, ingredient):
    qty = []
    for word in words:
        match = re.match(r'^\d+/\d+$', word)
        if word.isdigit() or match is not None:
            qty.append(word)
    if len(qty) == 0:
        qty = "N/A"
    else:
        qty = " ".join(qty)
    return qty
