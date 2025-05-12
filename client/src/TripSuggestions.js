// 📁 TripSuggestions.js
import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import DisplayMap from './DisplayMap';
import Loader from './Loader';
import SuggestionCard from './SuggestionCard';
import './TripSuggestions.css';

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
      const fetched = response.data.suggestions;
      setSuggestions(fetched);
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

  const handleClick = suggestion => setSelectedSuggestion(suggestion);

  return (
    <div className="trip-container">
      <h2 className="trip-title">🌍 Fun Trip Suggestions</h2>

      {error && <p className="error-msg">{error}</p>}
      {!location && <p className="info-msg">📍 Getting your location...</p>}
      {loading && <Loader />}

      {!loading && !selectedSuggestion && suggestions.length > 0 && (
        <div className="suggestion-list">
          {suggestions.map((s, idx) => (
            <SuggestionCard key={idx} suggestion={s} onClick={handleClick} />
          ))}
        </div>
      )}

      {!loading && !selectedSuggestion && location && (
        <button className="try-again-button" onClick={fetchSuggestions}>
          🔄 Try Again
        </button>
      )}

      {!loading && selectedSuggestion && (
        <div className="details-section">
          <h3>{selectedSuggestion.title}</h3>
          <p className="highlight"><strong>📝 Overview:</strong> {selectedSuggestion.info}</p>

          <div className="extra-details">
            <p>⏰ <strong>Estimated Time:</strong> {selectedSuggestion.estimated_time}</p>
            <p>💸 <strong>Estimated Cost:</strong> ${selectedSuggestion.estimated_cost}</p>
          </div>

          <div className="map-container">
            <h4>🗺️ Suggested Places to Visit:</h4>
            <ul>
              {selectedSuggestion.places.map((place, i) => (
                <li key={i}>🔹 {place}</li>
              ))}
            </ul>

            <DisplayMap userLocation={location} places={selectedSuggestion.places} />
          </div>

          <button className="back-button" onClick={() => setSelectedSuggestion(null)}>
            🔙 Back to Suggestions
          </button>
        </div>
      )}
    </div>
  );
};

export default TripSuggestions;
