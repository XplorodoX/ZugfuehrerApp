import React from 'react';
import './StationsDropdown.css';

const StationsDropdown = ({ stops }) => {
  return (
    // creates the stations overview in the timetable cards dropdown
    <div className="stops-container">
      {stops.map((stop, index) => (
        <div key={index} className="stop">
          <div className="stop-column station-name">{stop.destination}</div>
          <div className="stop-column station-times">
            Ankunft: {stop.arrival_time}
          </div>
          <div className="stop-column station-times">
            Abfahrt: {stop.departure_time}
          </div>
        </div>
      ))}
    </div>
  );
};

export default StationsDropdown;