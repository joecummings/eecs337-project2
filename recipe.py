from util import find_nth
import nltk

class recipe:
    def __init__ (self):
        self.url = ""
        self.name = ""
        self.ingredients = []
        self.directions = []
        self.methods = []
        self.tools = [[]]
        self.refineHa = True

    def refine(self):

        #Check
        if not self.refineHa:
            print("Already Refined")
            return None

        
        #Refine
        print("Refinining ...")

        new_ingredients = []
        for unparsed_ing in self.ingredients:
            n = find_nth(unparsed_ing," ",2)
            quantity, unit = unparsed_ing[:n].split( )
            name = unparsed_ing[n::].strip()
            new_ingredients.append((quantity,unit,name))
        self.ingredients = new_ingredients

        for unparsed_dir in self.directions:
            text = nltk.word_tokenize(unparsed_dir)
            print(nltk.pos_tag(text))



        
        

        #Lock It - Haha worst lock of all time
        self.refineHa = False

class ingredient:
    def __init__(self,originalString):
        self.name = ""
        self.quantity = 0
        self.measurement = ''
        self.unitType = '' #Like American or not
        self.healthy = 0 # Use Bools to represent how this ingredient does
        self.vegan = 0
        self.cuisine = 0