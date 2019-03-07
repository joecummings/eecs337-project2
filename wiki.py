
import requests
import json
import pickle

def hasNumbers(inputString):
  return any(char.isdigit() for char in inputString)

def pull_wikidata_food():
  query = '''PREFIX wikibase: <http://wikiba.se/ontology#>
      PREFIX wd: <http://www.wikidata.org/entity/>
      PREFIX wdt: <http://www.wikidata.org/prop/direct/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      
      SELECT ?foodLabel WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    ?food wdt:P279* wd:Q2095.
  }
      '''
  corpus = {
    "ingredients": {},
    "measurements": {},
    "techniques":{} 
  }
  url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
  data = requests.get(url, params={'query': query, 'format': 'json'}).json()
  for i in data['results']['bindings']:
    if i['foodLabel']['value'].lower() == "mozarella":
      print("HI")
    if not hasNumbers(i['foodLabel']['value'].lower()):
      corpus['ingredients'][i['foodLabel']['value'].lower()] = True
  return corpus


def pull_wikidata_meat():
  query = '''PREFIX wikibase: <http://wikiba.se/ontology#>
      PREFIX wd: <http://www.wikidata.org/entity/>
      PREFIX wdt: <http://www.wikidata.org/prop/direct/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      
      SELECT ?foodLabel ?subLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    ?food wdt:P279* wd:Q10990.
    OPTIONAL{?sub wdt:P279  ?food}
}
      '''
  meats = set([])
  url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
  data = requests.get(url, params={'query': query, 'format': 'json'}).json()
  for i in data['results']['bindings']:
    if not hasNumbers(i['foodLabel']['value'].lower()):
      meats.add(i['foodLabel']['value'].lower())
    if i.get('subLabel') is not None and not hasNumbers(i['subLabel']['value'].lower()) and i['subLabel']['value'].lower() != "":
      meats.add(i['subLabel']['value'].lower())
  return meats


def pull_all_vegetables():
  query1 = '''PREFIX wikibase: <http://wikiba.se/ontology#>
      PREFIX wd: <http://www.wikidata.org/entity/>
      PREFIX wdt: <http://www.wikidata.org/prop/direct/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      
     SELECT ?foodLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?food wdt:P279* wd:Q11004
}
limit 1000
      '''
  query2 = '''
  PREFIX wikibase: <http://wikiba.se/ontology#>
      PREFIX wd: <http://www.wikidata.org/entity/>
      PREFIX wdt: <http://www.wikidata.org/prop/direct/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      
  SELECT ?foodLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?food wdt:P279 wd:Q20136
}
limit 1000
  '''
  veggies = set([])
  url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
  data = requests.get(url, params={'query': query1, 'format': 'json'}).json()

  for i in data['results']['bindings']:
    if not hasNumbers(i['foodLabel']['value'].lower()):
      veggies.add(i['foodLabel']['value'].lower())

  data= requests.get(url, params={'query': query2, 'format': 'json'}).json()

  for i in data['results']['bindings']:
    if not hasNumbers(i['foodLabel']['value'].lower()):
      veggies.add(i['foodLabel']['value'].replace(" ", "_"))

    with open("vegetables.json") as file:
        data = json.load(file)
        for i in data['vegetables']:
          veggies.add(i)

  return veggies




# with open('ingredients.pickle', 'wb') as handle:
#         pickle.dump(movies, handle, protocol=pickle.HIGHEST_PROTOCOL)