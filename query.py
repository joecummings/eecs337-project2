
import sys
import requests
from bs4 import BeautifulSoup
import scraper as s
import re
query = ""


def main():
    if len(sys.argv) != 2:
        print("Please provide a recipe url to scrape.")
    else:
        query = sys.argv[1]
        print("Recipe Link: {0}".format(query))
        page = requests.get(query).text
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

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext.strip()

if __name__ == "__main__":
    main()
