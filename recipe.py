from nltk import MWETokenizer, sent_tokenize
import json
import re
import string
import scraper as s
import wiki
import pickle
ingredients = set([])
tokenizer = MWETokenizer()
utensil_tokenizer = MWETokenizer()
measurements = set([])
techniques = set([])


mexican = {}
chinese = {}
food = set([])
with open('healthy.pickle', 'rb') as handle:
        healthy = pickle.load(handle)

def type(food,foodtypes):
    possibleHits = food.split()
    for h in possibleHits:
        for key in foodtypes.keys():
            if h in key:
                return (food,foodtypes[key])
    return (food,'untyped')

def pull_meat():
    meats = wiki.pull_wikidata_meat()
    unaccountedandfish = ['bison','oysters', 'cod', 'duck', 'pollock', 'herring', 'snapper', 'duck eggs', 'giblets', 'scallops', 'lobster', 'goose', 'crab', 'rabbit', 'lamb', 'clams', 'catfish', 'mussels', 'calamari', 'shrimp', 'sea bass', 'tuna', 'octopus', 'liver', 'turkey', 'porgy', 'swordfish', 'ground turkey', 'squid']
    [meats.add(x) for x in unaccountedandfish]
    return meats
def pull_veggies():
    veggies = wiki.pull_all_vegetables()
    return veggies
def pull_utensils():
    utensils = wiki.pull_wikidata_utensils();
    return utensils
def pull_wiki():
    res = wiki.pull_wikidata_food()
    return res
utensils = pull_utensils()
utensils.add('bowl')
meats = pull_meat()
veggies = pull_veggies()

def build_tokenizer():
    for i in food:
        s = i.split("_")
        tokenizer.add_mwe(s)
    for u in utensils:
        i = u.lower().split("_")
        utensil_tokenizer.add_mwe(i)

def load_ingredients():
    print("Loading...")
    wiki_ingredients = pull_wiki()
    for i in wiki_ingredients['ingredients']:
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

def organize_directions(s):
    referenced_utensils = set([])
    sent_list = sent_tokenize(s)
    print("")
    for s in sent_list:
        used = extract_utensils(s)
        referenced_utensils = referenced_utensils.union(used)
    return sent_list, referenced_utensils

def extract_utensils(sentence):
    used = set([])
    tokens = utensil_tokenizer.tokenize(sentence.replace(",","").split())
    for token in tokens:
        if token in utensils and token not in measurements:
            used.add(token)
    return used
def build_ingredient(s,index):
    #tags
    tags = {}
    tags['healthy'] = 1
    tags['mexican'] = 0
    tags['chinese'] = 0
    tags['vegetarian'] = 1
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

    with open('unhealthy.pickle', 'rb') as handle:
        unhealthy = pickle.load(handle)

    name = name.replace('_',' ')
    threshold = 10
    meats = pull_meat()
    for n in name.split():
        if n in meats:
            tags['vegetarian'] = 0
            break
    for n in name.split():
        if n in unhealthy:
            tags['healthy'] = 0
            break
    if name in mexican:
        if mexican[name] > threshold:
            tags['mexican'] = 1
    if name in chinese:
        if chinese[name] > threshold:
            tags['chinese'] = 1
    tags['type'] = type(name,types)[1]

        
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
