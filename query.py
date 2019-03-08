from recipe import recipe
import sys
import requests
from bs4 import BeautifulSoup
import re
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe
import json
import recipe as r
import wiki
query = ""



#FOR SAMPLE OUTPUT ---- Run: python query.py
def main():
    r.load_ingredients()
    r.build_tokenizer()
    r.load_corpus()

    if "-url" not in sys.argv:
        pullrecipes()
    else:
        query = sys.argv[sys.argv.index("-url")+1]
        print("Recipe Link: {0}".format(query))
        get_url(query)
        
def get_url(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    scrape_recipe(soup)
<<<<<<< HEAD
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe
=======
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe

def scrape_recipe(soup):
        # This is called when user wants to scrape for specific recipe site
        # Try functions were used to prevent any one element from stopping the operation
<<<<<<< HEAD
<<<<<<< HEAD

    retRecipe = recipe()

=======
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe
=======
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe
    try:
        rtitle = soup.find_all('h1')
        rtitle = cleanhtml(str(rtitle[0]))
    except:
        rtitle = 'NA'
<<<<<<< HEAD
<<<<<<< HEAD

    print("Recipe Title: {0}".format(rtitle))
    retRecipe.name = "{0}".format(rtitle)
    print(retRecipe.name)
=======
    recipe = r.Recipe(rtitle)
    # print("Recipe Title: {0}".format(rtitle))
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe
=======
    recipe = r.Recipe(rtitle)
    # print("Recipe Title: {0}".format(rtitle))
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe

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
    print("\nINGREDIENTS\n")
    
    ingredients = soup.find_all("span", {"itemprop": "recipeIngredient"})
    count = 1
    for i in ingredients:
<<<<<<< HEAD
<<<<<<< HEAD
        print(i) 
        retRecipe.ingredients.append(i)
=======
=======
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe
        ingredient = r.build_ingredient(cleanhtml(str(i)),count)
        recipe.add_ingredient(ingredient)
        ingredients[ingredients.index(i)] = cleanhtml(str(i))
        count+=1
    # except:
        # ingredients = "NA"

<<<<<<< HEAD
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe
=======
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe

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


<<<<<<< HEAD
<<<<<<< HEAD
    for d in directions:
        if d.strip() != "":
            print("{0}) {1}".format(directions.index(d)+1,d))
            retRecipe.directions.append("{0}) {1}".format(directions.index(d)+1,d))

    return retRecipe
=======
    for d in recipe.get_steps():
        print("{0}".format(d))
    print()
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe
=======
    for d in recipe.get_steps():
        print("{0}".format(d))
    print()
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
<<<<<<< HEAD
  return cleantext.strip()
=======
  return cleantext.strip()



def pullrecipes():
    print("Grabbing 10 Recipes")
    for i in range(8000,8010):
        url = "https://www.allrecipes.com/recipe/{0}/oooh-baby-chocolate-prune-cake/".format(i)
        get_url(url)
    

if __name__ == "__main__":
    main()
>>>>>>> 3806e8fc8af0634e9535d29c0744e4d547df8ebe
