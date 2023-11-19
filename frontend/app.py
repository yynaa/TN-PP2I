from flask import Flask, render_template
import folium
import sys

from backend.db.functions import fetch_Data

app = Flask(__name__)

@app.route('/')
def root():
    return '<h1>ULTRA MEGA SUPER WHEELCHAIR MAN SIMULATOR 2019</h1>'

@app.route('/map')
def mapLoader():
    """
    Loads the map page
    """
    m = folium.Map(location=[48.689, 6.2], zoom_start=13)

    for building in fetch_Data("backend/db/database.db", "Buildings"):
        folium.Marker(
            location=[building["GPS_lat"], building["GPS_long"]],
            popup=building["building_name"],
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    return m.get_root().render()

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)