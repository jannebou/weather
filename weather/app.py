from flask import Flask, render_template, request
import folium
import weatherAPI
from flask import Flask, render_template, request, jsonify
import folium, json, parse, requests

app = Flask(__name__)

onclickmarkerkoordinaatit = {}
onclickmarkerorder = 0

api_key:str = '56cc934fb67645ceb9b113527242901'
base_url:str = 'http://api.weatherapi.com/v1'
paketti:dict = {}

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

#view -> command palette -> python interpreter 3.12 jos ei toimi
@app.route('/')
def index():
    # Create a map centered at a specific location
    map_osm = folium.Map(location=[62.791668, 22.841667], zoom_start=12)

    # Render the HTML page containing the map
    return render_template('index.html', map=map_osm._repr_html_())

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


@app.route('/saatiedothaku', methods=['GET'])
def weatherinfo():
    global onclickmarkerkoordinaatit

    weather_data = {}
    for marker_id, coordinates in onclickmarkerkoordinaatit.items():
        lat_lon_string = f"{coordinates['latitude']},{coordinates['longitude']}"
        weather_data[marker_id] = get_weather(lat_lon_string)
    print(weather_data)
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)onclickmarkerorder = 0

app = Flask(__name__)

@app.route('/')
def index():
    # Create a map centered at a specific location
    map_osm = folium.Map(location=[62.791668, 22.841667], zoom_start=12)
    weather = weatherAPI.get_weather("Seinäjoki")
    # Save the map to a file
    #map_osm.save("templates/index.html")

    # Render the HTML page containing the map
    return render_template('index.html', map=map_osm._repr_html_())

@app.route('/klikkikoordinaatit', methods=['POST'])
def map():
    global onclickmarkerorder

    if request.method == 'POST':
        #tätä pitää kasvattaa, että tiedetään klikattujen markerien koordinaattien järjestys
        onclickmarkerorder += 1

        lat = request.form['lat']
        lon = request.form['lon']
        print("Koordinaatit - Latitude:", lat, "Longitude:", lon)

        #tallennetaan lat ja lon sanakirjaan
        onclickmarkerkoordinaatit[onclickmarkerorder] = {'latitude': lat, 'longitude': lon}
        print(onclickmarkerkoordinaatit)
        return 'Vastaanotetut koordinaatit - Latitude: {} Longitude: {}'.format(lat, lon)
    else:
        return 'Jotain meni vikaan.'

if __name__ == '__main__':
    app.run(debug=True)
