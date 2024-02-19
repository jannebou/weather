from flask import Flask, render_template
import folium

app = Flask(__name__)

#test

@app.route('/')
def index():
    # Create a map centered at a specific location
    map_osm = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

    # Save the map to a file
    map_osm.save("templates/map.html")

    # Render the HTML page containing the map
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
