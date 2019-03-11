import json
import pickle
from pprint import pprint

unhealthy = [
    'canola oil',
    'corn oil',
    'soybean oil',
    'vegetable oil',
    'peanut oil',
    'sunflower oil',
    'safflower oil',
    'cottonseed oil',
    'grapeseed oil',
    'margarine',
    'shortening',
    'lamb',
    'beef',
    'pork',
    'bacon',
    'salami',
    'high fructose corn syrup',
    'white rice',
    'flour',
    'mayonaise',
    'trail mix',
    'fruit juice',
    'soda',
    'pop',
    'cola',
    'fried',
    'cereal',
    'white sugar',
    'pie',
    'frosting',
    'sausage'
]

uhealthy_dict = {h:1 for h in unhealthy}

with open('unhealthy.pickle', 'wb') as handle:
    pickle.dump(uhealthy_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('unhealthy.pickle', 'rb') as handle:
        types = pickle.load(handle)
pprint(types)