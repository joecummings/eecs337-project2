
import sys
import requests
from bs4 import BeautifulSoup
import re
import json
import recipe as r
query = ""



#FOR SAMPLE OUTPUT ---- Run: python query.py -nyc 500
def main():
    r.load_ingredients()
    r.load_corpus()
    if len(sys.argv) != 2:
        if "-nyc" in sys.argv:
            recipes = int(sys.argv[sys.argv.index("-nyc")+1])
            print("Supplementing ingredient list with {0} New York Times Cooking Recipes".format(recipes))
            r.ingredients = r.ingredients.union(r.pull_nyt(recipes))
        print("URL not correctly provided. Proceeding with test url's")
        pullrecipes()
    else:
        query = sys.argv[1]
        print("Recipe Link: {0}".format(query))
        get_url(query)
        
def get_url(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    scrape_recipe(soup)

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
    # print("Rating: {0} out of 5".format(starrating))

    try:
        reviewcount = soup.find_all("meta",{'itemprop':'reviewCount'})
        reviewcount = reviewcount[0]['content']
        recipe.set_number_of_reviews(reviewcount)
    except:
        reviewcount = 'NA'

    # print("Number of Reviews: {0}".format(reviewcount))

    try:
        calcount = soup.find_all("span",{"class":'calorie-count'})
        calcount = calcount[0]['aria-label']
        recipe.set_calories(calcount)
    except:
        calcount = 'NA'

    print("Calorie Count: {0}".format(calcount))

    # try: 
    print("\nINGREDIENTS:")

    ingredients = soup.find_all("span", {"itemprop": "recipeIngredient"})
    for i in ingredients:
        ingredient = r.build_ingredient(cleanhtml(str(i)))
        recipe.add_ingredient(ingredient)
        ingredients[ingredients.index(i)] = cleanhtml(str(i))
    # except:
        # ingredients = "NA"


    # for i in ingredients:
    #     print(i) 
    print()
    try:
        print("DIRECTIONS")

        directions = soup.find_all("span", {"class": "recipe-directions__list--item"})
        # print(directions)
        for i in directions:
            step = cleanhtml(str(i))
            if step.strip() != "":
                recipe.add_step(step)
    except:
        directions = "NA"


    for d in recipe.get_steps():
        print("{0}".format(d))
    print()

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
