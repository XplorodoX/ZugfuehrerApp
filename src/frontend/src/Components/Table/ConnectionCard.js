import React, { useState } from 'react';
import './ConnectionCard.css';
import StationsDropdown from './StationsDropdown';
// ConnectionCard component for displaying connection information
function ConnectionCard({ connection, onClick }) {
  const [isOpen, setIsOpen] = useState(false);
  const handleClick = () => {
    setIsOpen(!isOpen);
    if (onClick) {
      onClick();
    }
  }
  return (
    // displays a card containing the most important information about each connection
    <div className="connectionCard" onClick={handleClick}>
      <div className="gridContainer">
        <div className="connectionItem traintype">
          {connection.train_type}
        </div>
        <div className="connectionItem">
          {connection.departure_start} - {connection.arrival_destination}
        </div>
        <div className="connectionItem">
          Dauer: {connection.duration}
        </div>
        <div className="connectionItem">
          Gleis: {connection.plattform}
        </div>
        <div className="arrow-container">
          <i className={`arrow ${isOpen ? 'arrow-up' : ''}`} onClick={() => setIsOpen(!isOpen)}></i>
        </div>
      </div>
      {isOpen && (
        <div className={`additionalInfo ${isOpen ? 'expanded' : ''}`}>
          <br></br>
          <StationsDropdown stops={connection.stations}/>
        </div>
      )}
    </div>
  );
}
export default ConnectionCard;