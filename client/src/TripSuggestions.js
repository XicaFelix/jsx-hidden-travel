import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './TripSuggestions.css';
import DisplayMap from './DisplayMap';

const TripSuggestions = () => {
  const [location, setLocation] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [selectedSuggestion, setSelectedSuggestion] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => setLocation(position.coords),
        () => setError('📍 Unable to retrieve your location.')
      );
    } else {
      setError('❌ Geolocation is not supported by this browser.');
    }
  }, []);

  const fetchSuggestions = useCallback(() => {
    if (!location) return;

    setLoading(true);
    setError(null);
    setSelectedSuggestion(null);

    axios.post('http://127.0.0.1:5000/api/suggestions', {
      latitude: location.latitude,
      longitude: location.longitude
    })
      .then(response => {
        setSuggestions(response.data.suggestions || []);
        setLoading(false);
      })
      .catch(err => {
        setError('⚠️ Failed to fetch suggestions.');
        setLoading(false);
      });
  }, [location]);

  useEffect(() => {
    if (location) fetchSuggestions();
  }, [location, fetchSuggestions]);

  const handleSuggestionClick = (suggestion) => {
    setSelectedSuggestion(suggestion);
  };

  return (
    <div className="trip-container">
      <h2 className="trip-title">🌍 Fun Trip Suggestions</h2>
      {error && <p className="error-msg">{error}</p>}
      {!location && !error && <p>📍 Getting your location...</p>}
      {loading && <p>⏳ Fetching ideas...</p>}

      {!loading && !selectedSuggestion && suggestions.length > 0 && (
        <ul className="suggestion-list">
          {suggestions.map((suggestion, index) => (
            <li
              key={index}
              className="suggestion-item clickable"
              onClick={() => handleSuggestionClick(suggestion)}
            >
              🎯 {suggestion.title}
            </li>
          ))}
        </ul>
      )}

      {!loading && selectedSuggestion && (
        <div className="details-section">
          <h3>🌟 Adventure Details</h3>
          <p className="highlight">{selectedSuggestion.title}</p>
          <p>{selectedSuggestion.description}</p>

          <DisplayMap
            userLocation={location}
            suggestion={selectedSuggestion}
          />

          <button className="back-button" onClick={() => setSelectedSuggestion(null)}>
            🔙 Back to Suggestions
          </button>
        </div>
      )}
    </div>
  );
};

export default TripSuggestions;
