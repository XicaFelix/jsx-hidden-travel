import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)
CORS(app)

# Configure OpenAI client
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
            f"You are a creative local travel guide. The user is near {location} with a budget of {budget_range}. "
            f"Generate 3 unique trip ideas. For each one, return this structured format:\n\n"
            f"Title: [short name for the trip]\n"
            f"Info: [1-line teaser summary]\n"
            f"Places:\n"
            f"1. [Place 1 name] – [short activity or what to do there]\n"
            f"2. [Place 2 name] – [short activity or what to do there]\n"
            f"3. [Place 3 name] – [short activity or what to do there]\n"
            f"Estimated Time: [e.g., 3 hours]\n"
            f"Estimated Cost: [e.g., $25]\n\n"
            f"Only return 3 full suggestions, cleanly formatted."
        )

        completion = api.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful and structured travel planner."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=900
        )

        content = completion.choices[0].message.content
        suggestions_raw = content.strip().split("\n\n")

        suggestions = []
        for raw in suggestions_raw:
            item = {"places": []}
            lines = raw.split("\n")
            for line in lines:
                if line.startswith("Title:"):
                    item["title"] = line.replace("Title:", "").strip()
                elif line.startswith("Info:"):
                    item["info"] = line.replace("Info:", "").strip()
                elif line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
                    item["places"].append(line.strip())
                elif line.startswith("Estimated Time:"):
                    item["estimated_time"] = line.replace("Estimated Time:", "").strip()
                elif line.startswith("Estimated Cost:"):
                    item["estimated_cost"] = line.replace("Estimated Cost:", "").strip().replace("$", "")
            suggestions.append(item)

        return suggestions

    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True)
