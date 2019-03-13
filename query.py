import sys
import requests
from bs4 import BeautifulSoup
import re
import json
import recipe as r
import wiki
from transform import *
query = ""

def main():
    r.load_ingredients()
    r.build_tokenizer()
    r.load_corpus()

    query = input("Please provide an AllRecipes url: ")

    print("Recipe Link: {0}".format(query))
    recipe = get_url(query)
    # print_recipe(recipe)
    
    next_action = ""

    while next_action != 'x':
        if next_action == "":
            print_recipe(recipe)
        print("*** *** ***\n")
        print("Show Parsed Recipe Again-> p")
        print("Mexican -> m")
        print("Chinese -> c")
        print("Vegetarian -> v")
        print("Non-vegetarian -> n")
        print("Healthy -> h")
        print("Unhealthy -> u")
        print("Exit -> x")
        next_action = input("Select your next action/transformation: ")
        print("--- --- --- --- --- --- --- ---\n")
        if next_action == "p":
            next_action = ""
        else:
            new_recipe = perform_transform(next_action,recipe)
            print_recipe(new_recipe)
        
def print_recipe(r):
    print("\n*** *** ***")
    print("Recipe Title: {0}".format(r.name))
    # print("Calorie Count: {0}".format(r.calories))
    print("\nINGREDIENTS\n")
    for i,gred in enumerate(r.ingredients):
        print("Ingredient {0}".format(i))
        print("\tName: ", gred[1][0])
        if gred[1][2] != "":
            print("\tMeasurement: ", gred[1][2])
        if gred[1][1] != "":
            print("\tQuantity: ", gred[1][1], "\n")
            
    print("\nKITCHEN TOOLS")
    for tool in r.get_tools():
        print("\t"+ "- ",tool)
    print("\nCOOKING TECHNIQUES")
    print("\tPrimary: {0}".format(r.get_primary_method()))
    print("\tAll Techniques: {0}".format(list(r.get_methods())))
    # for m in r.get_methods():
    #     print("\t"+"- ", m)
    print("\nDIRECTIONS\n")
    for i, step in enumerate(r.steps):
        print("Step " + str(i + 1) + ") " + str(step.sentence))
        if len(step.ingredients) != 0:
            print("\tIngredients: " + str(step.ingredients))
        if len(step.tools) != 0:
            print("\tTools: "  + str(step.tools))
        if len(step.methods) != 0:
            print("\tMethods: "  + str(step.methods))
        if step.time != "N/A":
            print("\tTime: "  + str(step.time))
        print("")





def perform_transform(n,recipe):
    if n == 'x':
        exit(0)
    elif n == 'm':
        return transform_to_mexican(recipe)
    elif n == 'c':
        return transform_to_chinese(recipe)
    elif n == 'h':
        return transform_to_healthy(recipe)
    elif n == 'u':
        return transform_from_healthy(recipe)
    elif n == 'v':
        return transform_to_vegetarian(recipe)
    elif n == 'n':
        return transform_from_vegetarian(recipe)
    else:
        raise Exception("Command not found")
        
   
def get_url(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return scrape_recipe(soup)

def scrape_recipe(soup):
        # This is called when user wants to scrape for specific recipe site
        # Try functions were used to prevent any one element from stopping the operation
    try:
        rtitle = soup.find_all('h1')
        rtitle = cleanhtml(str(rtitle[0]))
    except:
        rtitle = 'NA'
    recipe = r.Recipe(rtitle)
    # print("Recipe Title: {0}".format(rtitle))

    try:
        starrating = soup.find_all('div',{'class':'rating-stars'})
        starrating = starrating[0]['data-ratingstars']
        recipe.set_rating(starrating)
    except:
        starrating = 'NA'

    try:
        reviewcount = soup.find_all("meta",{'itemprop':'reviewCount'})
        reviewcount = reviewcount[0]['content']
        recipe.set_number_of_reviews(reviewcount)
    except:
        reviewcount = 'NA'

    try:
        calcount = soup.find_all("span",{"class":'calorie-count'})
        calcount = calcount[0]['aria-label']
        recipe.set_calories(calcount)
    except:
        calcount = 'NA'

    # print("Calorie Count: {0}".format(calcount))

    # print("\nINGREDIENTS\n")
    
    ingredients = soup.find_all("span", {"itemprop": "recipeIngredient"})
    count = 1
    for i in ingredients:
        parsed_i = r.build_ingredient(cleanhtml(str(i)))
        recipe.add_ingredient([cleanhtml(str(i)), parsed_i])
        count+=1

    try:
        directions = soup.find_all("span", {"class": "recipe-directions__list--item"})
        utensils = set([])
        methods = set([])
        for i in directions:
            step = cleanhtml(str(i))
            if step.strip() != "" and "Watch Now" not in step:
                sentences = r.tokenize_step(step)
                for sentence in sentences:
                    uten, meth, ing, time = r.organize_directions(sentence)
                    for m in meth:
                        recipe.add_method(m.replace("_", " "))
                    utensils = utensils.union(uten)
                    # methods = methods.union(meth)
                    recipe.add_step(sentence, uten, meth, ing, time)
        for u in utensils:
            recipe.add_tool(u.replace("_"," "))
        # for m in methods:
        #     recipe.add_method(m.replace("_", " "))
    except:
        directions = "NA"

    return recipe

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext.strip()



def pullrecipes():
    print("Grabbing 10 Recipes")
    for i in range(8000,8010):
        url = "https://www.allrecipes.com/recipe/{0}/oooh-baby-chocolate-prune-cake/".format(i)
        get_url(url)
    

if __name__ == "__main__":
    main()
