from recipe import *
import pdb

with open('foodtypes.pickle', 'rb') as handle:
    foodtypes = pickle.load(handle)

meats = pull_meat()

transformations = {}
transformations['chinese'] = chinese
transformations['mexican'] = mexican

transformations['healthy'] = {h:1 for h in healthy}
transformations['unhealthy'] = {'greasy '+h:1 for h in healthy}

transformations['unvegetarian'] = {m:1 for m in meats}
transformations['vegetarian'] = {}
for k,v in foodtypes.items():
    if v == 'proteins':
        local_bool = True
        for n in k.split():
            if n in meats:
                local_bool = False
        if local_bool:
            transformations['vegetarian'][k] = 1


def transform_generic(transformation,r):
    new_recipe = Recipe(r.name + " - " + transformation)
    for ingredient in r.ingredients:
        #un transfromations
        if transformation[:2] == 'un':
            if ingredient[1][3][transformation[2::]] == 0:
                new_recipe.add_ingredient(ingredient)   
            else:
                new_ingredient = swap_ingredient(ingredient, transformation)
                new_recipe.add_ingredient(new_ingredient)
        #normal
        else:
            if ingredient[1][3][transformation] == 1:
                new_recipe.add_ingredient(ingredient)   
            else:
                new_ingredient = swap_ingredient(ingredient, transformation)
                new_recipe.add_ingredient(new_ingredient)
    return new_recipe

def transform_to_vegetarian(r):
    return transform_generic("vegetarian",r)

def transform_from_vegetarian(r):
    return transform_generic("unvegetarian",r)

def transform_to_healthy(r):
    return transform_generic("healthy",r)

def transform_from_healthy(r):
    return transform_generic("unhealthy",r)

def transform_to_mexican(r):
    return transform_generic("mexican",r)

def transform_to_chinese(r):
    return transform_generic("chinese",r)

def type(food):
    possibleHits = food.split()
    for h in possibleHits:
        if h in foodtypes:
            return (food,foodtypes[h])
    return (food,'untyped')

def swap_ingredient(i, t):

    #variables
    type_of_food = i[1][3]['type']
    threshold = 3
    list_of_relevant_transformations = transformations[t]

    #if its untyped do nothing
    if type_of_food == 'untyped':
        return i

    #start casing on it
    if t == 'chinese' or t == 'mexican':
        #filter for threshold
        list_of_relevant_transformations= [k for (k,v) in list_of_relevant_transformations.items() if v > threshold]
        #type them
        list_of_relevant_transformations = list(map(type,list_of_relevant_transformations))
        #filter by type
        list_of_relevant_transformations = [k for (k,v) in list_of_relevant_transformations if v == type_of_food]

        try:
            og_name = i[1][0]
            i[1][0] = list(list_of_relevant_transformations.keys())[0]
            del transformations[t][i[1][0]] #trim the dict, rerun every time
            i[0] = i[1][1]+' '+i[1][2]+' '+i[1][0]
        except:
            pass
    elif t == 'unhealthy':
        pass
    elif t == 'unvegetarian':

        if type_of_food != 'proteins':
            return i

        if i[1][3][t[2:]] == 1:
            try:
                og_name = i[1][0]
                i[1][0] = list(list_of_relevant_transformations.keys())[0]
                del transformations[t][i[1][0]] #trim
                i[0] = i[1][1]+' '+i[1][2]+' '+i[1][0]
            except:
                pass
    elif t == 'healthy':
        pass
    elif t == 'vegetarian':
        if i[1][3][t] == 0:
            try:
                og_name = i[1][0]
                i[1][0] = list(list_of_relevant_transformations.keys())[0]
                del transformations[t][i[1][0]] #trim
                i[0] = i[1][1]+' '+i[1][2]+' '+i[1][0]
            except:
                pass
    return i




