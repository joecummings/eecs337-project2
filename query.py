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
        print("Mexican -> m")
        print("Chinese -> c")
        print("Vegetarian -> v")
        print("Non-vegetarian -> n")
        print("Healthy -> h")
        print("Unhealthy -> u")
        print("Exit -> x")
        next_action = input("Select your next action/transformation: ")
        print("--- --- --- --- --- --- --- ---\n")
        new_recipe = perform_transform(next_action,recipe)
        print_recipe(new_recipe)
        
def print_recipe(r):
    print("\n*** *** ***")
    print("Recipe Title: {0}".format(r.name))
    print("Calorie Count: {0}".format(r.calories))
    print("\nINGREDIENTS\n")
    for i,gred in enumerate(r.ingredients):
        print("\t"+ str(i+1) + ") " + str(gred[0]))
    print("\nDIRECTIONS\n")
    for s in r.steps:
        print(s)

def perform_transform(n,recipe):
    if n == 'x':
        return
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
        parsed_i = r.build_ingredient(cleanhtml(str(i)),count)
        recipe.add_ingredient([cleanhtml(str(i)), parsed_i])
        count+=1

    try:
        # print("DIRECTIONS")
        directions = soup.find_all("span", {"class": "recipe-directions__list--item"})
        # print(directions)
        for i in directions:
            step = cleanhtml(str(i))
            if step.strip() != "":
                recipe.add_step(step)
    except:
        directions = "NA"

    # for d in recipe.get_steps():
    #     print("{0}".format(d))
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
