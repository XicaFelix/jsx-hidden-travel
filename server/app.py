from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("OPENAI_API_KEY")
base_url = "https://api.aimlapi.com/v1"
api = OpenAI(api_key=api_key, base_url=base_url)

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not latitude or not longitude:
        return jsonify({"error": "Invalid location data"}), 400

    location = f"Latitude: {latitude}, Longitude: {longitude}"
    budget_range = "$20–40"
    suggestions = get_trip_suggestions(location, budget_range)

    return jsonify({"suggestions": suggestions})

def get_trip_suggestions(location, budget_range):
    try:
        user_prompt = (
            f"You are a fun and adventurous local guide. The user is currently near {location} "
            f"and has a budget of {budget_range}. Suggest 3 unique and quirky things to do nearby — "
            f"like hidden gems, cool spots, fun activities, or surprising experiences. "
            f"Make sure the ideas are creative and memorable, not tourist clichés."
        )

        completion = api.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a creative travel assistant."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=400,
            n=1
        )

        content = completion.choices[0].message.content
        lines = [line.strip("-• ").strip() for line in content.split("\n") if line.strip()]
        
        # Dummy coordinates; in production use geocoding API
        suggestions = []
        sample_coords = [
            (37.7749, -122.4194),  # San Francisco
            (37.8044, -122.2712),  # Oakland
            (37.6879, -122.4702)   # Daly City
        ]
        
        for i, line in enumerate(lines[:3]):
            suggestions.append({
                "title": line,
                "latitude": sample_coords[i][0],
                "longitude": sample_coords[i][1]
            })

        return suggestions
    except Exception as e:
        print(f"Error during OpenAI call: {e}")
        return [{"title": "⚠️ Sorry, we couldn't generate suggestions.", "latitude": 0, "longitude": 0}]
    
if __name__ == '__main__':
    app.run(debug=True)
