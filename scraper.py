import requests
from bs4 import BeautifulSoup
import re
import json

start = 1020000
end = 1021000


def pull_ingredients(recipes):
    ingredients = set([])
    for i in range(start, start+recipes):
        res = get_url("https://cooking.nytimes.com/recipes/{0}".format(i))
        ingredients = ingredients.union(res)
    return ingredients
# To scrape NYT subscription


def get_url(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    ingredients = scrape_ingredients(soup)
    return ingredients

def scrape_ingredients(soup):
        # This is called when user wants to scrape for specific recipe site
        # Try functions were used to prevent any one element from stopping the operation
    ingredients = soup.find_all("span", {"class": "ingredient-name"})
    res = set([])
    if ingredients != []:
        for ingredient in ingredients:
            match = re.findall(r'>(.*)<', str(ingredient))
            if match != []:
                res.add(match[0])
    return res

