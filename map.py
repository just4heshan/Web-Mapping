import folium
from numpy import DataSource
import pandas

data = pandas.read_csv("Volcanoes.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22 volcano" target="_blank" rel="noopener noreferrer" target="_blank">%s</a><br>
Height: %s m<br>
Latitude : %s <br>
Longitude : %s
"""

def elev_color(height):
        if height > 3000:
            return "red"
        elif 1000 < height <=30000:
            return "orange"
        else:
            return "green"

map = folium.Map(location=[38.58, -112.09], zoom_start=6, tiles="Stamen Terrain")

fg_v = folium.FeatureGroup(name="Volcanoes")

for lt,ln,elv, nm in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (nm, nm, elv, lt, ln), width=200, height=100)
    fg_v.add_child(folium.CircleMarker(location=[lt, ln], radius= 6, popup=folium.Popup(iframe), fill_color=elev_color(elv), color = "grey", fill_opacity = 0.9))

fg_p = folium.FeatureGroup(name="Population")

fg_p.add_child(folium.GeoJson(data = open("world.json", 'r', encoding= 'utf-8-sig').read(), 
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red' }))

map.add_child(fg_p)
map.add_child(fg_v)
map.add_child(folium.LayerControl())

map.save("My_map.html")

