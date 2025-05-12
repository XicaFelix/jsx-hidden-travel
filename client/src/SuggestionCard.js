// 📁 SuggestionCard.js
import React from 'react';
import './SuggestionCard.css';

const SuggestionCard = ({ suggestion, onClick }) => {
  return (
    <div className="card" onClick={() => onClick(suggestion)}>
      <div className="content">
        <div className="img">
          <svg width="60" viewBox="0 0 512 512" className="icon">
            <circle cx="256" cy="256" r="256" fill="#f4b400" />
            <path d="M128 256h256v32H128z" fill="#fff"/>
          </svg>
        </div>
        <div className="description">
          <p className="title"><strong>{suggestion.title}</strong></p>
          <p className="info">{suggestion.description?.slice(0, 60)}...</p>
          <p className="price">${suggestion.estimated_cost || '20.00'}</p>
          <p className="info">{suggestion.estimated_time || '2-4 hrs'}</p>
        </div>
      </div>
    </div>
  );
};

export default SuggestionCard;
