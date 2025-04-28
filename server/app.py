import os
import random
import math
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Overpass API URL
OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

# Define place types and their Overpass tags
PLACE_TYPES = [
    ('amenity', 'cafe'),
    ('tourism', 'museum'),
    ('tourism', 'attraction'),
    ('leisure', 'park'),
    ('leisure', 'garden'),
    ('shop', 'mall'),
    ('amenity', 'restaurant'),
    ('amenity', 'fast_food'),
    ('shop', 'bakery'),
    ('tourism', 'viewpoint'),
    ('natural', 'beach'),
    ('tourism', 'theme_park'),
    ('tourism', 'gallery')
]

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    print(f"Received location: Latitude = {latitude}, Longitude = {longitude}")

    if latitude is None or longitude is None:
        return jsonify({"error": "Invalid location data"}), 400

    location = f"Latitude: {latitude}, Longitude: {longitude}"
    budget_range = "$20–40"

    suggestions = get_trip_suggestions(location, budget_range, latitude, longitude)

    return jsonify({"suggestions": suggestions})

def get_trip_suggestions(location, budget_range, latitude, longitude):
    try:
        print(f"Generating trip suggestions for {location} with budget {budget_range}")

        nearby_places = get_nearby_places(latitude, longitude)

        if len(nearby_places) < 2:
            return ["Not enough places found nearby to create suggestions."]

        dynamic_suggestions = []
        for _ in range(3):  # Generate 3 dynamic suggestions
            place1, place2 = random.sample(nearby_places, 2)

            # Smarter suggestion based on place type
            suggestion = create_suggestion(place1, place2)
            dynamic_suggestions.append(suggestion)

        return dynamic_suggestions

    except Exception as e:
        print(f"Error: {e}")
        return ["Sorry, we couldn't generate suggestions at the moment."]

def get_nearby_places(latitude, longitude):
    # First, detect how dense the area is
    density_query = f"""
    [out:json];
    way["highway"](around:1000,{latitude},{longitude});
    out;
    """

    try:
        density_response = requests.get(OVERPASS_API_URL, params={'data': density_query})
        density_data = density_response.json()
        roads_count = len(density_data.get('elements', []))

        # Decide radius based on density
        if roads_count > 50:
            search_radius = 1500  # Dense city
        elif roads_count > 20:
            search_radius = 2500  # Suburban
        else:
            search_radius = 4000  # Rural

        print(f"Detected {roads_count} roads. Using search radius: {search_radius} meters.")

        # Now build the real Overpass query
        query_parts = []
        for key, value in PLACE_TYPES:
            query_parts.append(f'node["{key}"="{value}"](around:{search_radius},{latitude},{longitude});')
        
        overpass_query = f"""
        [out:json];
        (
            {" ".join(query_parts)}
        );
        out;
        """

        response = requests.get(OVERPASS_API_URL, params={'data': overpass_query})
        data = response.json()

        places = []
        for element in data.get('elements', []):
            name = element['tags'].get('name')
            if name:
                places.append({
                    'name': name,
                    'tags': element['tags']
                })

        return places

    except Exception as e:
        print(f"Error fetching nearby places: {e}")
        return []

def create_suggestion(place1, place2):
    name1 = place1['name']
    name2 = place2['name']
    tags1 = place1['tags']
    tags2 = place2['tags']

    type1 = next((value for key, value in tags1.items() if key in ['amenity', 'tourism', 'leisure', 'shop', 'natural']), 'place')
    type2 = next((value for key, value in tags2.items() if key in ['amenity', 'tourism', 'leisure', 'shop', 'natural']), 'place')

    # --- Smart suggestions based on combinations ---
    if type1 == "cafe" and type2 == "museum":
        return f"☕ Start your day sipping coffee at {name1}, then immerse yourself in art at {name2}!"
    if type1 == "cafe" and type2 == "park":
        return f"🌸 Grab a coffee at {name1} and enjoy a peaceful stroll at {name2}."
    if type1 == "park" and type2 in ["restaurant", "fast_food", "bakery"]:
        return f"🌳 After a refreshing walk at {name1}, recharge with a meal at {name2}."
    if type1 == "beach" and type2 in ["restaurant", "fast_food", "bakery"]:
        return f"🏖️ Chill at {name1} and savor some tasty food at {name2} nearby!"
    if type1 == "bakery" and type2 == "beach":
        return f"🥐 Grab a pastry from {name1} and head to {name2} for a picnic by the waves."
    if type1 == "theme_park" and type2 == "viewpoint":
        return f"🎢 After thrilling rides at {name1}, wind down with epic views at {name2}."
    if type1 == "gallery" and type2 == "cafe":
        return f"🎨 Explore art at {name1} and chat about your favorite pieces over coffee at {name2}."
    if type1 == "viewpoint" and type2 in ["restaurant", "cafe"]:
        return f"🌄 Capture breathtaking views from {name1}, then indulge yourself at {name2}."
    if type1 == "museum" and type2 == "restaurant":
        return f"🏛️ Discover fascinating exhibits at {name1}, followed by a delicious meal at {name2}."
    if type1 == "mall" and type2 in ["restaurant", "cafe"]:
        return f"🛍️ Shop 'til you drop at {name1}, then fuel up at {name2}."

    # --- More creative random fallback templates ---
    fallback_templates = [
        f"🎯 Plan a chill day starting at {name1} and wrapping up with a cozy visit to {name2}.",
        f"🚶‍♂️ Stroll through {name1}, then treat yourself at {name2}!",
        f"📸 Capture the vibes at {name1}, then enjoy a relaxing time at {name2}.",
        f"🌟 Explore {name1}'s charm before heading over to {name2} for a fun break!",
        f"🎉 Start your adventure at {name1}, and celebrate the day at {name2}!",
        f"🍀 Discover hidden gems at {name1}, then savor good food at {name2}.",
        f"🎈 Take it easy at {name1}, and spice things up with a visit to {name2}!",
        f"🎒 Begin a mini-adventure at {name1} and recharge at {name2}."
    ]

    return random.choice(fallback_templates)

if __name__ == '__main__':
    app.run(debug=True)
