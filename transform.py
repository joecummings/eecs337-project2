from recipe import *
import pdb
transformations = {}
transformations['chinese'] = chinese


with open('foodtypes.pickle', 'rb') as handle:
        foodtypes = pickle.load(handle)

def transform_generic(transformation,r):
    new_recipe = Recipe(r.name + " - " + transformation)
    for ingredient in r.ingredients:
        #if its already of the type skip it
        if ingredient[1][3][transformation] == 1:
            new_recipe.add_ingredient(ingredient)
        else:
            new_ingredient = swap_ingredient(ingredient, transformation)
            new_recipe.add_ingredient(new_ingredient)
    return new_recipe

def transform_to_vegetarian(r):
    return transform_generic("vegetarian",r)

def transform_to_healthy():
    return transform_generic("healthy",r)

def transform_to_mexican():
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

    #filter for threshold
    list_of_relevant_transformations= [k for (k,v) in list_of_relevant_transformations.items() if v > threshold]
    #type them
    list_of_relevant_transformations = list(map(type,list_of_relevant_transformations))
    #filter by type
    list_of_relevant_transformations = [k for (k,v) in list_of_relevant_transformations if v == type_of_food]
    
    og_name = i[1][0]
    i[1][0] = list_of_relevant_transformations[0]
    i[0] = i[1][1]+' '+i[1][2]+' '+i[1][0]
    return i

    # Right here we need to find the ingredients that match this type of food

    # Next, we need to use that subset of ingredients to find the set of foods that match the target transformations

    # Then we return the new ingredient

