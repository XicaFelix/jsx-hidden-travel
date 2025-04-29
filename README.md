
# 🌎 Trip Adventure Generator

![React](https://img.shields.io/badge/Frontend-React-blue?logo=react)  
![Flask](https://img.shields.io/badge/Backend-Flask-green?logo=flask)  
![License](https://img.shields.io/badge/License-MIT-yellow)  
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

_"Find mini-adventures around you with one click!"_

---

## 📖 User Journey

When users visit the app:
- They are greeted with a **clean, lively React UI**.
- The app **requests their location** immediately.
- A **loading spinner** creates anticipation while adventures are being prepared.
- After a few seconds, users see **3 creative, personalized suggestions** for fun mini-trips nearby.
- Suggestions feel like **spontaneous, fun trip ideas** — not boring lists.
- Users can **refresh suggestions** anytime with a button — no page reloads.
- The frontend has **smooth animations**, **emoji-rich text**, and a **mobile-first responsive design**.

---

## ⚙️ Tech Stack

| Frontend | Backend | Other |
|:---|:---|:---|
| React.js  | Python Flask | Overpass API (OpenStreetMap) |
| React Hooks (useState, useEffect) | Flask-CORS | Geolocation API (Browser) |
| CSS Animations | REST API | Fetch API |

---

## ✨ Features

### Frontend (React)

- **Browser location request** on app load.
- **Loading spinner** while fetching adventure suggestions.
- **Animated adventure cards** with fun phrases.
- **Refresh button** to load new adventures.
- **Responsive layout** for mobile and desktop users.
- **Friendly, emoji-rich, creative UI**.

---

### Backend (Flask)

- Accepts **latitude** and **longitude** from the frontend.
- Uses **Overpass API** to find nearby:
  - Cafes ☕
  - Parks 🌳
  - Restaurants 🍽️
  - Landmarks 🏛️
- Randomly generates **creative adventure 

---



---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/XicaFelix/jsx-hidden-travel.git
cd jsx-hidden-travel
```

---

### 2. Set up the Backend

```bash
cd server
python -m venv venv
source venv/bin/activate    # (Linux/macOS)
venv\Scripts\activate       # (Windows)

pip install -r requirements.txt

python app.py
```

Backend runs at: `http://127.0.0.1:5000`

---

### 3. Set up the Frontend

```bash
cd clinet
npm install
npm start
```

Frontend runs at: `http://localhost:3000` 

---

## 🔥 Example Adventure Suggestions

- 🎯 🛶 Paddle around Lake Park, then grab coffee at Sunny Beans Cafe!
- 🎯 🖼️ Explore Downtown Art Museum, then relax at Blossom Bistro!
- 🎯 🌳 Chill at Green Meadows Park, then savor pastries at The Cozy Corner!

---

## 📸 Sample Screenshots

| Home Page | Adventure Suggestions |
|:---|:---|
| ![Home Screenshot](frontend/public/home-screenshot.png) | ![Adventure Screenshot](frontend/public/adventure-screenshot.png) |



---

## 🛠 Future Improvements

🌟 AI-Powered Trip Suggestions:
Integrate an AI model that personalizes adventure ideas based on the user's interests, time of day, weather, and past choices for even smarter suggestions!

🌟 Interactive Map Previews:
Show trip locations visually on an embedded map (using Mapbox or Leaflet.js).

🌟 Save Favorite Adventures:
Let users bookmark and view their favorite suggestions.

🌟 Mood-Based Filters:
Allow users to choose their mood (Relax, Adventure, Eat, Explore) and tailor suggestions accordingly.

🌟 Shareable Adventure Cards:
Allow users to share adventure suggestions directly via social media or links.


---



> _Life’s too short for boring weekends. Discover your next mini-adventure now!_

---

