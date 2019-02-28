# This file will contain all of the functions necessary to parse the beautifulsoup response text
def clean():
    print("DO STUFF")

def scrape_recipe(br, year, idnumber):
    # This is called when user wants to scrape for specific recipe site
    # Try functions were used to prevent any one element from stopping the operation

    # recipe title
    try:
        rtitle = br.find_element_by_tag_name('h1').text
    except:
        rtitle = 'NA'

    # Star rating
    try:
        starrating = br.find_element_by_class_name('rating-stars').\
            get_attribute('data-ratingstars')
    except:
        starrating = 'NA'

    # Number of people who clicked that they "made it"
    try:
        madeitcount = br.find_element_by_class_name('made-it-count').text
    except:
        madeitcount = 'NA'

    # Number of reviews
    try:
        reviewcount = br.find_element_by_class_name('review-count').text
        reviewcount = str(re.findall('(\w+) reviews', reviewcount)[0])
    except:
        reviewcount = 'NA'

    # calories per serving
    try:
        calcount = br.find_element_by_class_name('calorie-count').text
        calcount = str(re.findall('(\w+) cals', calcount)[0])
    except:
        calcount = 'NA'

    # prep time
    try:
        prepTime = br.find_element_by_xpath('//time[@itemprop = "prepTime"]').\
            get_attribute('datetime')
        prepTime = str(re.findall('PT(\w+)', prepTime)[0])
    except:
        prepTime = 'NA'

    # Cook time
    try:
        cookTime = br.find_element_by_xpath('//time[@itemprop = "cookTime"]').\
            get_attribute('datetime')
        cookTime = str(re.findall('PT(\w+)', cookTime)[0])
    except:
        cookTime = 'NA'

    # total time
    try:
        totalTime = br.find_element_by_xpath('//time[@itemprop = "totalTime"]').\
            get_attribute('datetime')
        totalTime = str(re.findall('PT(\w+)', totalTime)[0])
    except:
        totalTime = 'NA'
    # find all the ingredient attributes
    ingred = br.find_elements_by_class_name("checkList__item")
