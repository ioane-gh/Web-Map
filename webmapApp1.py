import folium
import pandas


# checks what color the clicker should be
def color_by_height(height):
    if height < 1000:
        return "green"
    elif 1000 <= height <= 3000:
        return "orange"
    else:
        return "red"


# creating a map object
my_map = folium.Map([41.719049959229324, 44.786658999470966], zoom_start=6)

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

# creating a feature group for volcanoes
fg_volcano = folium.FeatureGroup(name="volcano")

# adds circle markers on the map
for lt, ln, el in zip(lat, lon, elev):
    color = color_by_height(el)
    fg_volcano.add_child(folium.CircleMarker(location=(lt, ln), popup=str(el) + " m", radius=6,
                                             fill_color=color_by_height(el), color="grey", fill_opacity=0.7))


# creating a feature group for population
fg_population = folium.FeatureGroup(name="population")
# adding colors by population
fg_population.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
                                       style_function=lambda x: {
                                           "fillColor": "green" if x["properties"]["POP2005"] < 10000000
                                           else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000
                                           else "red"}))

# adding feature groups to map object
my_map.add_child(fg_volcano)
my_map.add_child(fg_population)

# adding layer control to the map object
my_map.add_child(folium.LayerControl())

my_map.save("map.html")
