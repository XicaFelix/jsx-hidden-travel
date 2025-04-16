import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './TripSuggestions.css';

const TripSuggestions = () => {
  const [location, setLocation] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch user's location on page load
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => {
          setLocation(position.coords);
        },
        err => {
          setError('📍 Unable to retrieve your location.');
        }
      );
    } else {
      setError('❌ Geolocation is not supported by this browser.');
    }
  }, []);

  // Fetch suggestions based on user location
  const fetchSuggestions = useCallback(() => {
    if (!location) return;

    setLoading(true);
    setError(null);
    axios
      .post('http://127.0.0.1:5000/api/suggestions', {
        latitude: location.latitude,
        longitude: location.longitude
      })
      .then(response => {
        setSuggestions(response.data.suggestions);
        setLoading(false);
      })
      .catch(err => {
        setError('⚠️ Failed to fetch suggestions.');
        console.error('Error details:', err);
        setLoading(false);
      });
  }, [location]);

  // Trigger suggestions when location is first fetched
  useEffect(() => {
    if (location) {
      fetchSuggestions();
    }
  }, [location, fetchSuggestions]);

  return (
    <div className="trip-container">
      <h2 className="trip-title">🌍 Fun Trip Suggestions</h2>

      {error && <p className="error-msg">{error}</p>}
      {!error && !location && <p className="info-msg">📍 Getting your location...</p>}
      {loading && <p className="info-msg">⏳ Fetching ideas for your trip...</p>}

      {!loading && suggestions.length > 0 && (
        <ul className="suggestion-list">
          {suggestions.map((suggestion, index) => (
            <li key={index} className="suggestion-item">🎯 {suggestion}</li>
          ))}
        </ul>
      )}

      {!loading && location && (
        <button className="try-again-button" onClick={fetchSuggestions}>
          🔄 Try Again
        </button>
      )}
    </div>
  );
};

export default TripSuggestions;
