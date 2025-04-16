import React from 'react';
import './App.css';
import TripSuggestions from './TripSuggestions';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to Trip Suggestions!</h1>
      </header>
      <main>
        <TripSuggestions />
      </main>
    </div>
  );
}

export default App;
