
import sys
import requests
from bs4 import BeautifulSoup
import scraper as s
import re
from query import scrape_recipe
query = ""


def main():

    # Perform Query
    if len(sys.argv) != 2:
        print("Please provide a recipe url to scrape.")
    else:
        query = sys.argv[1]
        print("Recipe Link: {0}".format(query))
        page = requests.get(query).text
        soup = BeautifulSoup(page, 'html.parser')
        old_recipe = scrape_recipe(soup)
        old_recipe.refine()
        

    # Interface with the user - Judge me.
    print('1) Type v to make this recipe vegetarian')
    print('2) Type h to make  this recipe healthy')
    print('3) Type c to make this recipe CUISINE')
    type = input("wtf")

    if type == 'v':
        print('hii')
    elif type == 'h':
        print('hhii')
    elif type == 'c':
        print('hhhii')
    else:
        print("You're not using this correctly.")
        return None

    print('hi')



if __name__ == "__main__":
    main()
