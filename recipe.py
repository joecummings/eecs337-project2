from nltk import MWETokenizer
import json
import re
import string
import scraper as s
import wiki
import pickle
import pdb
ingredients = set([])
tokenizer = MWETokenizer()
measurements = set([])
techniques = set([])
meats = set([])
veggies = set([])
mexican = {}
chinese = {}
food = set([])
healthy_fats = ['olive oil', 'sunflower oil', 'soybean oil', 'corn oil',  'sesame oil',  'peanut oil']
healthy_protein = [ 'peas',  'beans', 'eggs', 'crab', 'fish','chicken', 'tofu', 'liver', 'turkey']
healthy_dairy = [ 'fat free milk', 'low fat milk', 'yogurt',  'low fat cheese']
healthy_salts = ['low sodium soy sauce', 'sea salt', 'kosher salt']
healthy_grains = ['oat cereal', 'wild rice', 'oatmeal', 'whole rye', 'buckwheat', 'rolled oats', 'quinoa','bulgur', 'millet', 'brown rice', 'whole wheat pasta']
healthy_sugars = ['real fruit jam', 'fruit juice concentrates', 'monk fruit extract', 'cane sugar', 'molasses', 'brown rice syrup' 'stevia', 'honey', 'maple syrup', 'agave syrup', 'coconut sugar', 'date sugar', 'sugar alcohols', 'brown sugar']
healthy = healthy_dairy + healthy_fats + healthy_grains + healthy_protein + healthy_salts + healthy_sugars

def pull_meat():
    meats = wiki.pull_wikidata_meat()
    unaccounted = ['duck', 'goose', 'turkey', 'ground turkey', 'lamb', 'bison', 'rabbit', 'liver', 'giblets', 'duck eggs', 'catfish', 'cod', 'flounder', 'haddock', 'halibut', 'herring', 'mackerel', 'pollock', 'porgy', 'sea bass', 'snapper', 'swordfish', 'trout', 'tuna', 'clams', 'crab', 'crayfish', 'lobster', 'mussels', 'octopus', 'oysters', 'scallops', 'squid', 'calamari', 'shrimp']
    [meats.add(x) for x in unaccounted]
    return meats
def pull_veggies():
    veggies = wiki.pull_all_vegetables()
    return veggies
def pull_wiki():
    res = wiki.pull_wikidata_food()
    return res

def build_tokenizer():
    for i in food:
        s = i.split("_")
        tokenizer.add_mwe(s)
    
def load_ingredients():
    print("Loading...")
    wiki_ingredients = pull_wiki()
    for i in wiki_ingredients['ingredients']:
        food.add(i.replace(" ", "_"))
    meats = pull_meat()
    for i in meats:
        food.add(i.replace(" ", "_"))
    veggies = pull_veggies()
    for veggie in veggies:
        food.add(i.replace(" ", "_"))
    with open("ingredients.json") as file:
        data = json.load(file)
        for i in data:

            if i['cuisine'] == 'mexican':
                for ingredient in i['ingredients']:

                    ingredient = ingredient.replace("_", " ")

                    if ingredient in mexican:
                        mexican[ingredient] += 1
                    else:
                        mexican[ingredient] = 1

            if i['cuisine'] == 'chinese':
                for ingredient in i['ingredients']:

                    ingredient = ingredient.replace("_", " ")

                    if ingredient in chinese:
                        chinese[ingredient] += 1
                    else:
                        chinese[ingredient] = 1

            for ingredient in i['ingredients']:
                food.add(ingredient.replace(" ", "_"))  


def load_corpus():
    with open("corpus.json") as file:
        data = json.load(file)
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


def build_ingredient(s,index):
    #tags
    tags = {}
    tags['veggie'] = 0
    tags['meat'] = 0
    ####
    tags['healthy'] = 0
    tags['mexican'] = 0
    tags['chinese'] = 0
    tags['vegetarian'] = 0
    tags['type'] = ''

    match = re.search(r'\((.*?)\)', s)
    if match is not None:
        alternate_measurement = match.groups()[0]
        s = s.replace("(" + alternate_measurement + ")", "")
    else:
        alternate_measurement = "N/A"
    phrase = s.replace(",", "").lower()
    words = tokenizer.tokenize(phrase.split())
    preparation = ""
    name = tag_ingredient_name(words)

    with open('foodtypes.pickle', 'rb') as handle:
        types = pickle.load(handle)

    name = name.replace('_',' ')
    threshold = 3
    meats = pull_meat()
    for n in name.split():
        if n in meats:
            tags['meat'] = 1
            break
    if name in mexican:
        if mexican[name] > threshold:
            tags['mexican'] = 1
    if name in chinese:
        if chinese[name] > threshold:
            tags['chinese'] = 1
    if name in types.keys():
        tags['type'] = types[name]
    else:
        tags['type'] = 'untyped'
        
    quantity = tag_ingredient_quantity(words, name)
    sent = " ".join(words)
    sent = sent.replace(quantity, "")
    sent = sent.replace(name, "")
    words = sent.split()
    measurement = tag_ingredient_measurement(words)
    sent = " ".join(words)
    sent = sent.replace(measurement, "")
    
    return [name.replace("_"," "), quantity, measurement,tags]

def tag_ingredient_measurement(words):
    measure = ""
    for word in words:
        if word in measurements:
            measure = word
    return measure
    

def tag_ingredient_name(words):
    name = ""
    for word in words:
        if word in food:
            name = word
    return name


def tag_ingredient_quantity(words, ingredient):
    qty = []
    for word in words:
        match = re.match(r'^\d+/\d+$', word)
        if word.isdigit() or match is not None:
            qty.append(word)
    if len(qty) == 0:
        qty = ""
    else:
        qty = " ".join(qty)
    return qty
