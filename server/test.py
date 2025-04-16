from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the model only once
generator = pipeline("text-generation", model="gpt2")

@app.route('/api/suggestions', methods=['POST'])
def suggest():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    prompt = f"Suggest a fun travel destination near the location ({latitude}, {longitude}) with budget tips."

    # Generate response
    ai_response = generator(prompt, max_length=60, do_sample=True, temperature=0.7)[0]['generated_text']

    # Post-process if needed
    return jsonify({'suggestions': [ai_response.strip()]})

if __name__ == '__main__':
    app.run(debug=True)
