import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI  # Use OpenAI client with AIMLAPI

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Set up OpenAI (AIMLAPI) configuration
api_key = os.getenv("OPENAI_API_KEY")
base_url = "https://api.aimlapi.com/v1"

# Print key (for debugging - remove in production)
print(f"API KEY: {api_key}")

# Initialize OpenAI API client
api = OpenAI(api_key=api_key, base_url=base_url)

# Route to get trip suggestions
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


# Function to generate travel ideas using AIMLAPI
def get_trip_suggestions(location, budget_range):
    try:
        user_prompt = (
            f"You are a fun and adventurous local guide. The user is currently near {location} "
            f"and has a budget of {budget_range}. Suggest 3 unique and quirky things to do nearby — "
            f"like hidden gems, cool spots, fun activities, or surprising experiences. "
            f"Make sure the ideas are creative and memorable, not tourist clichés."
        )

        completion = api.chat.completions.create(
            model="gpt-4o",  # Or use "gpt-3.5-turbo" if needed
            messages=[
                {"role": "system", "content": "You are a creative travel assistant."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=400,
            n=1
        )

        content = completion.choices[0].message.content
        activities = [item.strip("-• ").strip() for item in content.split("\n") if item.strip()]
        return activities[:3]

    except Exception as e:
        print(f"Error during OpenAI call: {e}")
        return ["⚠️ Sorry, we couldn't generate suggestions at the moment."]


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
