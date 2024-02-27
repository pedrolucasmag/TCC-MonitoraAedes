import requests
import os
from geopy import geocoders

municipio = os.getenv("MUNICIPIO")
GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")
g = geocoders.GoogleV3(api_key=GMAPS_API_KEY)

def get_address_by_coordinates(lat, long):
    location = g.reverse(f"{lat}, {long}")
    return location.raw

def get_address_location(form):
    error_message = {"error":f"Endereço residencial inválido ou não pertence ao município de {municipio}!"}
    cep_api = requests.get(f'https://viacep.com.br/ws/{form.data["cep"]}/json/')

    if cep_api.status_code == 400:
        return {"error": "CEP inválido!"}
    
    cep_data = cep_api.json()

    if cep_data["localidade"] != municipio:
        return error_message

    rua = cep_data["logradouro"]
    bairro = cep_data["bairro"]

    restrictedComponents = {"country":"BR"}
    location = g.geocode(f'{form.data["rua"]} - {form.data["numero"]}, {municipio}, {form.data["cep"]}', components= restrictedComponents,timeout=3, exactly_one=True)

    locationConfidence = location.raw['geometry']['location_type']

    if location == None or locationConfidence == 'APPROXIMATE':
        return error_message

    lat = location.latitude
    long = location.longitude
    
    return {"rua": rua, "bairro": bairro, "lat": lat, "long": long}