
import sys
import requests
from bs4 import BeautifulSoup
import scraper as s
import re
import pdb
#import transformers
query = ""
request = ""


def main():
    if len(sys.argv) != 2:
        print("Please provide a recipe url to scrape and any modifications you want to make")
    else:
        query = sys.argv[1]
        print("Recipe Link: {0}".format(query))
        page = requests.get(query).text
        soup = BeautifulSoup(page, 'html.parser')
        scrape_recipe(soup)
        #pdb.set_trace()
        request = input("Okay, how do you want to alter this recipe?")
        #request = sys.argv[2]
        transformation_query(request)


def scrape_recipe(soup):
        # This is called when user wants to scrape for specific recipe site
        # Try functions were used to prevent any one element from stopping the operation

    try:
        rtitle = soup.find_all('h1')
        rtitle = cleanhtml(str(rtitle[0]))
    except:
        rtitle = 'NA'

    print("Recipe Title: {0}".format(rtitle))

    try:
        starrating = soup.find_all('div',{'class':'rating-stars'})
        starrating = starrating[0]['data-ratingstars']
    except:
        starrating = 'NA'
    print("Rating: {0} out of 5".format(starrating))

    try:
        reviewcount = soup.find_all("meta",{'itemprop':'reviewCount'})
        reviewcount = reviewcount[0]['content']
    except:
        reviewcount = 'NA'

    print("Number of Reviews: {0}".format(reviewcount))

    try:
        calcount = soup.find_all("span",{"class":'calorie-count'})
        calcount = calcount[0]['aria-label']
    except:
        calcount = 'NA'

    print("Calorie Count: {0}".format(calcount))

    try:
        ingredients = soup.find_all("span", {"itemprop": "recipeIngredient"})
        for i in ingredients:
            ingredients[ingredients.index(i)] = cleanhtml(str(i))
    except:
        ingredients = "NA"

    print("INGREDIENTS:")

    for i in ingredients:
        print(i)

    try:
        directions = soup.find_all("span", {"class": "recipe-directions__list--item"})
        for i in directions:
            directions[directions.index(i)] = cleanhtml(str(i))
    except:
        directions = "NA"

    print("DIRECTIONS")

    for d in directions:
        if d.strip() != "":
            print("{0}) {1}".format(directions.index(d)+1,d))

def transformation_query(word):
    #Determine Type of transformation requested
    #print("Okay, how do you want to alter this recipe?")
    #request = input("Okay, how do you want to alter this recipe?")
    #parse each response to see if it contains a key word related to each potential
    #task also check to see if capitalization matters
    request = str(word)
    if "vegetarian" in request:
        print("got a veggie request") #replace with call to vegetarian modifier function
    elif "healthy" in request:
        print("got a healthy request") #replace with call to healthier modifier function
    elif "family" in request:
        print("got a family request") #replace with call to family style modifier function (double everything)
    elif "mexican" in request:
        print("got a mexican request") #replace with call to spicy modifier function (double everything)
    else:
        print("Sorry, but the cookbook doesn't have any suggestions for that!")

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext.strip()

if __name__ == "__main__":
    main()
