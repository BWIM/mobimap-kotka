import json
import geojson
from shapely.geometry import shape, Polygon
from shapely.ops import unary_union
import requests
from geopy.distance import geodesic


# Load GeoJSON file
def load_geojson(file_path):
    with open(file_path) as f:
        return geojson.load(f)


# Get center of multipolygon
def get_multipolygon_centroid(multipolygon):
    # Convert the geometry into a shapely MultiPolygon
    geom = shape(multipolygon)

    if isinstance(geom, Polygon):
        # If it's a MultiPolygon, find the centroid of all the polygons combined
        return geom.centroid
    return None


# Calculate the duration using Valhalla API for a batch of 100 features
def get_duration_via_valhalla(sources, targets, profile):
    try:
        valhalla_base_url = "http://localhost:8002"
        j = {
            "sources": sources,
            "targets": targets,
            "costing": profile["mode"]["key"],
            "costing_options": profile["costing_options"],
            "date_time": {"type": 1, "value": "2024-06-18T08:00"},
        }
        query = f"{valhalla_base_url}/sources_to_targets?json={json.dumps(j)}"
        response = requests.get(query)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error with Valhalla request: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error with Valhalla request: {e}")
        return None


# Save results back to GeoJSON
def save_geojson(file_path, data):
    with open(file_path, "w") as f:
        geojson.dump(data, f)


# Main function to process geojson in batches of 100
def process_geojson(file_path, output_path, point_of_origin, profile, batch_size=100):
    geo_data = load_geojson(file_path)

    sources = [{"lat": point_of_origin["lat"], "lon": point_of_origin["lon"]}]
    targets = []
    feature_batches = []
    sum_features = len(geo_data["features"])
    counter = 0

    for feature in geo_data["features"]:
        # Get centroid of each multipolygon
        centroid = get_multipolygon_centroid(feature["geometry"])
        if centroid:
            targets.append({"lat": centroid.y, "lon": centroid.x})
            feature["properties"]["center"] = [centroid.x, centroid.y]
            feature_batches.append(feature)

            # When we reach the batch size (100), make the API call
            if len(targets) == batch_size:
                process_batch(feature_batches, sources, targets, profile)
                # Clear the batch and start a new one
                targets.clear()
                feature_batches.clear()

        counter += 1
        print(
            f"Processed {counter} out of {sum_features} features: {counter / sum_features * 100:.2f}%"
        )

    # Process remaining features if any
    if targets:
        process_batch(feature_batches, sources, targets, profile)

    # Save updated geojson
    save_geojson(output_path, geo_data)


# Helper function to process a batch of features
def process_batch(feature_batch, sources, targets, profile):
    try:
        mode = "pedestrian"
        valhalla_result = get_duration_via_valhalla(sources, targets, profile)

        if valhalla_result:
            durations = valhalla_result.get("sources_to_targets", [])
            for i, feature in enumerate(feature_batch):
                if not feature.get("properties", {}).get(mode, None):
                    feature["properties"][mode] = {}
                if durations and len(durations[0]) > i:
                    # Extracting the duration (assuming this is the value returned)
                    time = durations[0][i].get("time", None)
                    if time:
                        feature["properties"][mode]["duration"] = time / 60
                    feature["properties"][mode]["distance"] = durations[0][i].get(
                        "distance", None
                    )

                else:
                    feature["properties"][mode]["duration"] = None
        else:
            # If there's an error, mark the duration as None for this batch
            for feature in feature_batch:
                feature["properties"]["duration"] = None
    except Exception as e:
        print(f"Error processing batch: {e}")

# Example usage
if __name__ == "__main__":
    geojson_input = "hexagons_smoller.geojson"
    geojson_output = "output.geojson"

    # Point of origin (source point)
    point_of_origin = {
        "lat": 60.470794698765665,
        "lon": 26.94807370982602,
    }  # Example: Paris

    # Valhalla profile
    profile = {
        "mode": {"key": "pedestrian"},
        "costing_options": {},
    }

    process_geojson(geojson_input, geojson_output, point_of_origin, profile)
