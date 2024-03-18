from flask import Flask, render_template, request
import folium
import weatherAPI
import koordinaatitJaKuvat

onclickmarkerkoordinaatit = {}
onclickmarkerorder = 0

kelikameroidenKoordinaatit = koordinaatitJaKuvat.getKoordinaatit()
kelikameroidenKuvat = koordinaatitJaKuvat.getKuvat()

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
