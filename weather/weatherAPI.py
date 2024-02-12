"""
Toimii kutsumalla "get_weather("KaupunginNimi tai koordinaatit")"
"""
import requests
import json
import parse

api_key:str = '56cc934fb67645ceb9b113527242901'
base_url:str = 'http://api.weatherapi.com/v1'
paketti:dict = {}


def get_weather(city:str)-> dict:
    """ 
    Palauttaa sanakirjamuodossa olevan paketin josta löytyy säätiedot,
    haku toimii Kaupungin nimellä tai koordinaateilla
    """
    city = city.capitalize()
    endpoint = f'/current.json?key={api_key}&q={city}'
    url = base_url + endpoint
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
    
        name = data["location"]["name"]
        temp = data["current"]["temp_c"]
        temp_feels_like = data["current"]["feelslike_c"]
        visibility = data["current"]["vis_km"]
        wind = data["current"]["wind_kph"]
        wind_dir = data["current"]["wind_dir"]
        air_pressure = data["current"]["pressure_mb"]
        condition = data["current"]["condition"]["text"]


        # print("kaupunki: ",name)
        # print("lämpötila: ", temp, "°c")
        # print("tuntuu kuin: ",temp_feels_like, "°c")
        # print("näkyvyys: ", visibility, "km")
        # print("tuuli: ", wind, "km/h")
        # print("tuulen suunta: ", wind_dir)
        # print("ilman paine: ", air_pressure )
        # print("tila: ", condition)




        paketti = {
            "nimi" : name,
            "lämpötila" : temp,
            "tuntuu kuin" : temp_feels_like,
            "näkyvyys" : visibility,
            "tuuli" : wind,
            "tuulen suunta" : wind_dir,
            "ilman paine" : air_pressure,
            "säätila" : condition,
        }

        return paketti

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")


def main()->None:
    print(get_weather("Seinäjoki"))

# pa = get_weather(input())
if __name__ == "__main__":
    main()
