import requests
from pprint import pprint
import pymongo

url = 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/hospitales/hospitales.geojson'
response = requests.get(url)
objeto = response.json()
cliente = pymongo.MongoClient("mongodb://172.21.0.2:27017/")
bd = cliente['salud']
coleccion = bd['hospitales']
coleccion.insert_many(objeto['features'])