from recipe import *
from types import *

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

def swap_ingredient(i, t):
    type_of_food = i[3]['type']
    possible_swaps = types["type_of_food"]
    # Right here we need to find the ingredients that match this type of food
    # Next, we need to use that subset of ingredients to find the set of foods that match the target transformations
    # Then we return the new ingredient

