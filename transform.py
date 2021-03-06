from recipe import *
import copy
from random import choice 

with open('foodtypes.pickle', 'rb') as handle:
    foodtypes = pickle.load(handle)

with open('unhealthy.pickle', 'rb') as handle:
    unhealthy = pickle.load(handle)

meats = pull_meat()

transformations = {}
transformations['chinese'] = chinese
transformations['mexican'] = mexican

transformations['healthy'] = {h:1 for h in healthy}
transformations['unhealthy'] = unhealthy

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
    '''
    Parameters:
        transformation (string): type of transformation to make
        r (Recipe): old recipe
    Returns:
        new recipe (Recipe)
    '''
    new_recipe = Recipe(r.name + " - " + transformation)
    new_steps = copy.deepcopy(r.steps)

    for ingredient in r.ingredients:
        #un transfromations
        if transformation[:2] == 'un':
            if ingredient[1][3][transformation[2::]] == 0:
                new_recipe.add_ingredient(ingredient)   
            else:
                new_ingredient = swap_ingredient(ingredient, transformation)
                new_recipe.add_ingredient(new_ingredient)
                for i,s in enumerate(new_steps):
                    for j,ingred in enumerate(new_steps[i].ingredients):
                        if ingred == ingredient[1][0]:
                            new_steps[i].ingredients[j] = new_ingredient[1][0]
                    new_steps[i].sentence = new_steps[i].sentence.replace(ingredient[1][0], new_ingredient[1][0])
        #normal
        else:
            if ingredient[1][3][transformation] == 1:
                new_recipe.add_ingredient(ingredient)
            else:
                new_ingredient = swap_ingredient(ingredient, transformation)
                new_recipe.add_ingredient(new_ingredient)
                for i,s in enumerate(new_steps):
                    for j,ingred in enumerate(new_steps[i].ingredients):
                        if ingred == ingredient[1][0]:
                            new_steps[i].ingredients[j] = new_ingredient[1][0]
                    new_steps[i].sentence = new_steps[i].sentence.replace(ingredient[1][0], new_ingredient[1][0])
    
    for t in r.get_tools():
        new_recipe.add_tool(t)
    
    for s in new_steps:
        new_recipe.add_step(s.sentence,s.tools,s.methods,s.ingredients,s.time)
    
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

#Single Param
def type(food):
    possibleHits = food.split()
    for h in possibleHits:
        for key in foodtypes.keys():
            if h in key:
                return (food,foodtypes[key])
    return (food,'untyped')

def swap_ingredient(i, t):

    i = copy.deepcopy(i)

    #variables
    type_of_food = i[1][3]['type']
    threshold = 3
    list_of_relevant_transformations = transformations[t]

    #if its untyped do nothing
    if type_of_food == 'untyped':
        return i

    #start casing on it
    if t == 'chinese' or t == 'mexican':
        #filter,type,filter
        list_of_relevant_transformations= [k for (k,v) in list_of_relevant_transformations.items() if v > threshold]
        list_of_relevant_transformations = list(map(type,list_of_relevant_transformations))
        list_of_relevant_transformations = [k for (k,v) in list_of_relevant_transformations if v == type_of_food]

        #make sure there's something
        if (len(list_of_relevant_transformations)) < 1:
            return i

        #swap
        og_name = i[1][0]
        i[1][0] = choice(list_of_relevant_transformations)
        del transformations[t][i[1][0]]
        i[0] = i[1][1]+' '+i[1][2]+' '+i[1][0]

    elif t == 'unhealthy':

        # if type_of_food != 'proteins' or type_of_food != 'oil':
        #     return i

        if i[1][3][t[2:]] == 0:
            return i
            
        list_of_relevant_transformations= [k for (k,v) in list_of_relevant_transformations.items()]
        list_of_relevant_transformations = list(map(type,list_of_relevant_transformations))
        list_of_relevant_transformations = [k for (k,v) in list_of_relevant_transformations if (v == 'proteins' or v == 'oil')]

        #make sure there's something
        if (len(list_of_relevant_transformations)) < 1:
            return i

        #swap
        og_name = i[1][0]
        i[1][0] = choice(list_of_relevant_transformations)
        del transformations[t][i[1][0]]
        i[0] = i[1][1]+' '+i[1][2]+' '+i[1][0]
            
    elif t == 'unvegetarian':

        if type_of_food != 'proteins':
            return i

        if i[1][3][t[2:]] == 0:
            return i
                
        og_name = i[1][0]
        i[1][0] = choice(list(list_of_relevant_transformations.keys()))
        del transformations[t][i[1][0]] #trim
        i[0] = i[1][1]+' '+i[1][2]+' '+i[1][0]

    elif t == 'healthy':

        if type_of_food != 'proteins' and type_of_food != 'oil':
            return i

        if i[1][3][t] == 1:
            return i
        
        list_of_relevant_transformations = [k for (k,v) in list_of_relevant_transformations.items()]
        list_of_relevant_transformations = list(map(type,list_of_relevant_transformations))
        list_of_relevant_transformations = [k for (k,v) in list_of_relevant_transformations if v == type_of_food]

        if len(list_of_relevant_transformations) < 1:
            return i
        
        og_name = i[1][0]
        i[1][0] = choice(list_of_relevant_transformations)
        del transformations[t][i[1][0]] #trim
        i[0] = i[1][1]+' '+i[1][2]+' '+i[1][0]

    elif t == 'vegetarian':

        if type_of_food != 'proteins':
            return i


        if i[1][3][t] == 1:
            return i

        og_name = i[1][0]
        i[1][0] = choice(list(list_of_relevant_transformations.keys()))
        del transformations[t][i[1][0]] #trim
        i[0] = i[1][1]+' '+i[1][2]+' '+i[1][0]

    return i




