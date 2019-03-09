from recipe import chinese,mexican

def transform_generic(transformation,r):
    for ingredient in r.ingredients:
        #if its already of the type skip it
        if ingredient[3][transformation] == 1:
            continue
        else:
            pass

def transform_to_vegetarian(r):
    return transform_generic("vegetarian",r)

def transform_to_healthy():
    return transform_generic("healthy",r)

def transform_to_mexican():
    return transform_generic("mexican",r)

def transform_to_chinese(r):
    return transform_generic("chinese",r)