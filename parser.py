import json
import pickle
from pprint import pprint

healthy_fats = ['olive oil', 'sunflower oil', 'soybean oil', 'corn oil',  'sesame oil',  'peanut oil']
healthy_protein = [ 'peas',  'beans', 'eggs', 'crab', 'fish','chicken', 'tofu', 'liver', 'turkey']
healthy_dairy = [ 'fat free milk', 'low fat milk', 'yogurt',  'low fat cheese']
healthy_salts = ['low sodium soy sauce', 'sea salt', 'kosher salt']
healthy_grains = ['oat cereal', 'wild rice', 'oatmeal', 'whole rye', 'buckwheat', 'rolled oats', 'quinoa','bulgur', 'millet', 'brown rice', 'whole wheat pasta']
healthy_sugars = ['real fruit jam', 'fruit juice concentrates', 'monk fruit extract', 'cane sugar', 'molasses', 'brown rice syrup' 'stevia', 'honey', 'maple syrup', 'agave syrup', 'coconut sugar', 'date sugar', 'sugar alcohols', 'brown sugar']
healthy = healthy_dairy + healthy_fats + healthy_grains + healthy_protein + healthy_salts + healthy_sugars

healthy_dict = {h:1 for h in healthy}
print(healthy_dict)
with open('healthy.pickle', 'wb') as handle:
    pickle.dump(healthy_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('healthy.pickle', 'rb') as handle:
        types = pickle.load(handle)
pprint(types)