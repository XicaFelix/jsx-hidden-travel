import os
import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

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

    suggestions = get_trip_suggestions(location, budget_range)

    return jsonify({"suggestions": suggestions})

def get_trip_suggestions(location, budget_range):
    try:
        print(f"Generating trip suggestions for {location} with budget {budget_range}")

        # Pool of possible adventures
        all_suggestions = [
            "🌲 Hike a hidden forest trail and bring snacks for a scenic picnic.",
            "🎨 Visit a funky art café and paint your own canvas.",
            "🚴‍♀️ Rent a bike and explore local murals or graffiti walls.",
            "🌌 Attend a local stargazing event or planetarium night.",
            "🧘 Join an outdoor yoga class in a park or rooftop.",
            "🧩 Try a puzzle-filled escape room nearby.",
            "🎭 Watch a local theater improv night.",
            "🚣 Kayak or paddleboard at a nearby lake or beach.",
            "🏞️ Discover a hidden waterfall or nature spot.",
            "🍔 Go on a food truck crawl and sample local eats.",
            "🕵️ Do a mystery-solving walking tour through the city.",
            "📷 Try an Instagram-worthy photo walk downtown."
        ]

        # Randomly pick 3 different suggestions
        return random.sample(all_suggestions, 3)

    except Exception as e:
        print(f"Error: {e}")
        return ["Sorry, we couldn't generate suggestions at the moment."]

if __name__ == '__main__':
    app.run(debug=True)
