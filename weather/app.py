from flask import Flask, render_template
import folium

app = Flask(__name__)

@app.route('/')
def index():
    # Create a map centered at a specific location
    map_osm = folium.Map(location=[62.791668, 22.841667], zoom_start=12)

    # Save the map to a file
    map_osm.save("templates/index.html")

    # Render the HTML page containing the map
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)