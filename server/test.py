import os
from flask import Flask, jsonify, request
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Setup OpenAI API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Route to get trip suggestions based on user's location
@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    data = request.get_json()

    # Get the latitude and longitude from the incoming request
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Log the received location for debugging
    print(f"Received location: Latitude = {latitude}, Longitude = {longitude}")

    # Validate if the latitude and longitude are present
    if not latitude or not longitude:
        return jsonify({"error": "Invalid location data"}), 400

    # Construct the location string (you can expand this with additional information)
    location = f"Latitude: {latitude}, Longitude: {longitude}"

    # Define a budget range (you can customize this further)
    budget_range = "$20–40"

    # Get suggestions from AI
    suggestions = get_trip_suggestions(location, budget_range)

    return jsonify({"suggestions": suggestions})

# Function to simulate AI-based trip suggestions
# Function to simulate AI-based trip suggestions with a creative prompt
def get_trip_suggestions(location, budget_range):
    try:
        # prompt for OpenAI
        prompt = f"""
        You're a fun and adventurous guide helping someone explore exciting things in their city. 
        They are currently near {location} and have a budget of {budget_range}. 
        Suggest a few cool, unique, and unforgettable activities they could do nearby. 
        Make sure the activities are fun, not too common, and ideally a little quirky or surprising. 
        Provide a variety of suggestions like visiting an unusual bar, a cool local event, a hidden gem, 
        or something out-of-the-ordinary like an interactive experience or an outdoor adventure. 
        Keep it light-hearted, spontaneous, and memorable, but also ensure it's something that can easily be done 
        without long wait times or overwhelming crowds. The suggestions should fit the vibe of a local explorer!
        """
        
        # Get AI-generated response from OpenAI with a more creative and engaging prompt
        response = openai.Completion.create(
            model="text-davinci-003",  # Or use a different model depending on your requirements
            prompt=prompt,
            max_tokens=200,  # Allow for more detail
            n=3,  # Get 3 suggestions
            stop=None,
            temperature=0.7,  # Higher value for more creative results
        )
        
        # Extract suggestions from the response
        suggestions = response.choices
        activities = [suggestion.text.strip() for suggestion in suggestions]

        # Return the list of suggested activities
        return activities

    except Exception as e:
        print(f"Error: {e}")
        return ["Sorry, we couldn't generate suggestions at the moment."]


# Main entry point for running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
