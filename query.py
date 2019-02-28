
import sys
import requests
from bs4 import BeautifulSoup
import scraper
query = ""

def main():
    if len(sys.argv) != 2:
        print("Please provide a recipe url to scrape.")
    else:
        query = sys.argv[1]
        print("Recipe Link: {0}".format(query))
        page = requests.get(query).text
        soup = BeautifulSoup(page,'html.parser')
        print(soup)


if __name__ == "__main__":
    main()
