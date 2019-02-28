# Asks user what kind of recipe transformation they want to do
import sys
import requests
from bs4 import BeautifulSoup
import scraper as s
import re

#Determine Type of transformation requested
print("Okay, how do you want to alter this recipe?")
request = sys.argv[1]

#parse each response to see if it contains a key word related to each potential
#task also check to see if capitalization matters

if request.search(vegetarian):
    pass() #replace with call to vegetarian modifier function
elif request.search(healthy):
    pass() #replace with call to healthier modifier function
elif request.search(family style):
    pass() #replace with call to family style modifier function (double everything)
elif request.search(spicy):
    pass() #replace with call to spicy modifier function (double everything)
else:
    print("Sorry, but the cookbook doesn't have any suggestions for that!")
