from flask import Flask, render_template, request, jsonify
import requests
import koordinaatitJaKuvat

app = Flask(__name__)

onclickmarkerkoordinaatit = {}
onclickmarkerorder = 0

api_key:str = '56cc934fb67645ceb9b113527242901'
base_url:str = 'http://api.weatherapi.com/v1'
paketti:dict = {}

#hakee nettisivulta json muodossa tiedot ja ne jaetaan sanakirjoihin
def get_weather(city:str):
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

        # Tietoikkunan pohja
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

#view -> command palette -> python interpreter 3.12 jos ei toimi, Kartta pohja
@app.route('/')
def index():

    # Renderöi HTML sivua, jossa on kartta
    return render_template('index.html')

#tallentaa klikatut koordinaatit
@app.route('/klikkikoordinaatit', methods=['POST'])
def map():
    global onclickmarkerorder

    if request.method == 'POST':
        #tätä pitää kasvattaa, että tiedetään asetettujen markerien koordinaattien järjestys
        onclickmarkerorder += 1

        lat = request.form['lat']
        lon = request.form['lon']
        print("Koordinaatit - Latitude:", lat, "Longitude:", lon)

        onclickmarkerkoordinaatit[onclickmarkerorder] = {'latitude': lat, 'longitude': lon}
        print(onclickmarkerkoordinaatit)
        return 'Vastaanotetut koordinaatit - Latitude: {} Longitude: {}'.format(lat, lon)
    else:
        return 'POST request expected.'

#hakee käyttäjän sijaintiin perustuvat säätiedot
@app.route('/kayttajasaatiedot', methods=['GET'])
def userweather():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    latlon = f"{lat},{lon}"
    weatherdata = get_weather(latlon)
    return jsonify(weatherdata)

#klikkikoordinaateista säätietoja
@app.route('/saatiedothaku', methods=['GET'])
def weatherinfo():
    global onclickmarkerkoordinaatit

    weather_data = {}
    for marker_id, coordinates in onclickmarkerkoordinaatit.items():
        lat_lon_string = f"{coordinates['latitude']},{coordinates['longitude']}"
        weather_data[marker_id] = get_weather(lat_lon_string)

    #print(weather_data)
    return jsonify(weather_data)

#kelikameroiden kuvat koordinaattien perusteella
@app.route('/kelikamerat', methods=['GET'])
def kelikamera():
    kelikameroidenKoordinaatit = koordinaatitJaKuvat.getKoordinaatit()
    image_urls = koordinaatitJaKuvat.getKuvat()
    data = []

    #yhdistä koordinaatit ja kuvien linkit
    for coord, url in zip(kelikameroidenKoordinaatit, image_urls):
        lon, lat, _ = coord
        data.append({'lat': lat, 'lon': lon, 'image_url': url})

    #printtaa datan
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)