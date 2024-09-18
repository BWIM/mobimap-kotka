import json
import folium
import geojson
from folium.plugins import MousePosition


# Load the processed GeoJSON file
def load_geojson(file_path):
    with open(file_path) as f:
        return geojson.load(f)


# Get color based on duration (in minutes)
def get_color(duration):
    if duration is None:
        return "transparent"
    elif duration < 15:
        return "#006400"  # Dark Green
    elif duration < 20:
        return "#00FF00"  # Light Green
    elif duration < 30:
        return "#FFFF00"  # Yellow
    elif duration < 45:
        return "#FFA500"  # Orange
    else:
        return "#FF0000"  # Red


# Create folium map and add hexagons
def create_map(geojson_data, output_map_path):
    # Define a map centered at a reasonable location (based on your geojson file)
    center_lat, center_lon = (
        60.4708,
        26.9481,
    )  # Example center (adjust based on your area)
    my_map = folium.Map(location=[center_lat, center_lon], zoom_start=10)

    # Add mouse position plugin to display lat/lon on hover
    formatter = "function(num) {return L.Util.formatNum(num, 5);};"
    mouse_position = MousePosition(
        position="topright",
        separator=" | ",
        empty_string="Unavailable",
        lng_first=True,
        num_digits=20,
        prefix="Coordinates:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    )
    my_map.add_child(mouse_position)

    # Add each feature (hexagon) to the map with appropriate color
    for feature in geojson_data["features"]:
        geometry = feature["geometry"]
        properties = feature["properties"]
        duration = properties.get("pedestrian", {}).get("duration", None)

        color = get_color(duration)

        if geometry["type"] == "Polygon":
            folium.GeoJson(
                geometry,
                style_function=lambda feature, color=color: {
                    "fillColor": color,
                    "color": "black",
                    "weight": 0.5,
                    "fillOpacity": 0.5 if color != "transparent" else 0,
                    "borderColor": "black",
                    "borderOpacity": 0.1,
                },
            ).add_to(my_map)

    # Save the map as an HTML file
    my_map.save(output_map_path)


# Main function
if __name__ == "__main__":
    geojson_file = "output.geojson"  # Your processed GeoJSON
    output_html = "map_walk_smol.html"  # Output HTML file

    # Load the geojson data
    geojson_data = load_geojson(geojson_file)

    # Create the map and save it to HTML
    create_map(geojson_data, output_html)

    print(f"Map saved as {output_html}")
