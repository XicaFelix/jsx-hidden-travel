import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './TripSuggestions.css';

const TripSuggestions = () => {
  const [location, setLocation] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [selectedSuggestion, setSelectedSuggestion] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [details, setDetails] = useState(null); // Details for selected suggestion

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
    setSelectedSuggestion(null);
    setDetails(null); // Reset details

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

  useEffect(() => {
    if (location) {
      fetchSuggestions();
    }
  }, [location, fetchSuggestions]);

  // Handler when a suggestion is clicked
  const handleSuggestionClick = (suggestion) => {
    setSelectedSuggestion(suggestion);

    // Generate random extra details
    const randomBudget = Math.floor(Math.random() * 200) + 50; // $50–250
    const randomHours = Math.floor(Math.random() * 4) + 2; // 2–5 hours

    setDetails({
      budget: randomBudget,
      hours: randomHours,
    });
  };

  return (
    <div className="trip-container">
      <h2 className="trip-title">🌍 Fun Trip Suggestions</h2>

      {error && <p className="error-msg">{error}</p>}
      {!error && !location && <p className="info-msg">📍 Getting your location...</p>}
      {loading && <p className="info-msg">⏳ Fetching ideas for your trip...</p>}

      {/* Show suggestions */}
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

      {/* Try again button */}
      {!loading && !selectedSuggestion && location && (
        <button className="try-again-button" onClick={fetchSuggestions}>
          🔄 Try Again
        </button>
      )}

      {/* Show selected suggestion details */}
      {!loading && selectedSuggestion && (
        <div className="details-section">
          <h3>🌟 Adventure Details</h3>
          <p className="highlight">✨ {selectedSuggestion}</p>

          {/* Extra Details */}
          {details && (
            <div className="extra-details">
              <p>💸 Estimated Budget: <strong>${details.budget}</strong></p>
              <p>⏰ Estimated Time Needed: <strong>{details.hours} hours</strong></p>
            </div>
          )}
          

          {/* Go back to the list of suggestions */}
          <button className="back-button" onClick={() => setSelectedSuggestion(null)}>
            🔙 Back to Suggestions
          </button>
        </div>
      )}
    </div>
  );
};

export default TripSuggestions;
