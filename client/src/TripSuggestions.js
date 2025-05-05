import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './TripSuggestions.css';

const TripSuggestions = () => {
  const [location, setLocation] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [selectedSuggestion, setSelectedSuggestion] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [details, setDetails] = useState(null);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => {
          setLocation(position.coords);
        },
        () => {
          setError('📍 Unable to retrieve your location.');
        }
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
    setDetails(null);

    axios.post('http://127.0.0.1:5000/api/suggestions', {
      latitude: location.latitude,
      longitude: location.longitude
    })
    .then(response => {
      setSuggestions(response.data.suggestions);
      setLoading(false);
    })
    .catch(err => {
      console.error('Error details:', err);
      setError('⚠️ Failed to fetch suggestions. Make sure the server is running.');
      setLoading(false);
    });
  }, [location]);

  useEffect(() => {
    if (location) {
      fetchSuggestions();
    }
  }, [location, fetchSuggestions]);

  const handleSuggestionClick = (suggestion) => {
    setSelectedSuggestion(suggestion);
      };

  return (
    <div className="trip-container">
      <h2 className="trip-title">🌍 Fun Trip Suggestions</h2>

      {error && <p className="error-msg">{error}</p>}
      {!error && !location && <p className="info-msg">📍 Getting your location...</p>}
      {loading && <p className="info-msg">⏳ Fetching ideas for your trip...</p>}

      {!loading && !selectedSuggestion && suggestions.length > 0 && (
        <ul className="suggestion-list">
          {suggestions.map((suggestion, index) => (
            <li
              key={index}
              className="suggestion-item clickable"
              onClick={() => handleSuggestionClick(suggestion)}
            >
              🎯 {suggestion}
            </li>
          ))}
        </ul>
      )}

      {!loading && !selectedSuggestion && location && (
        <button className="try-again-button" onClick={fetchSuggestions}>
          🔄 Try Again
        </button>
      )}

      {!loading && selectedSuggestion && (
        <div className="details-section">
          <h3>🌟 Adventure Details</h3>
          <p className="highlight">✨ {selectedSuggestion}</p>
          {details && (
            <div className="extra-details">
              <p>💸 Estimated Budget: <strong>${details.budget}</strong></p>
              <p>⏰ Estimated Time Needed: <strong>{details.hours} hours</strong></p>
            </div>
          )}
          <button className="back-button" onClick={() => setSelectedSuggestion(null)}>
            🔙 Back to Suggestions
          </button>
        </div>
      )}
    </div>
  );
};

export default TripSuggestions;
