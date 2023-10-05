import React from "react";
import "./timetable.css"
import ConnectionCard from '../Components/Table/ConnectionCard';


class Timetable extends React.Component {
    constructor(props) {
      super(props);
  
      this.state = {
        start_station: '',
        destination_station: '',
        date: new Date().toISOString().slice(0, 10),
        time: new Date().toISOString().slice(11,16),
        results: [],
        start_missing: false,
        destination_missing: false,
      };
    }

    startStations = [
      'Aalen Hbf',
      'Schwäbisch Gmünd',
      'Heidenheim',
      'Langenau(Württ)',
      'Ulm Hbf',
      'Schorndorf',
      'Stuttgart Hbf',
      'Nürnberg Hbf',
      'Ellwangen',
      'Donauwörth',
      'Waiblingen',
      'Crailsheim',
      'Karlsruhe Hbf',
      'Pforzheim Hbf',
      'Nördlingen',
      'Oberkochen',
      'München Hbf',
      'Augsburg Hbf',
  ]
  
    handleChange = (event) => {
      this.setState({ [event.target.id]: event.target.value });
    };
  
    handleSubmit = async (event) => {
      event.preventDefault();

      // Check if the start station is empty
      if (!this.state.start_station) {
        this.setState({ start_missing: true }); // Set the start_missing state to true if string1 is empty
      } else {
        this.setState({ start_missing: false }); // Set the start_missing state to false if string1 is not empty
      }

      if (!this.state.destination_station) {
        this.setState({ destination_missing: true }); // Set the destination_missing state to true if string1 is empty
      } else {
        this.setState({ destination_missing: false }); // Set the destination_missing state to false if string1 is not empty
      }

      // if any of both are empty we can return instantly
      if (this.state.start_missing || this.state.destination_missing) {
        return;
      }

      const datetime = `${this.state.date}T${this.state.time}`;

      const response = await this.sendRequestWithData(
        this.state.start_station,
        this.state.destination_station,
        datetime
      );
  
      // Update the results with the request response
      this.setState({ results: response });
    };
  
    sendRequestWithData = async (start_station, destination_station, datetime) => {
      // Implement your request logic here, using fetch() or other libraries like Axios to send the request
      // and include the input values.
      try {
        const response = await fetch('/timetable_submit', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            start_station: start_station,
            destination_station: destination_station,
            datetime: datetime,
          }),
        });
    
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        return data;
      } catch (error) {
        console.error('Error:', error);
        return [];
      }
    };
  
    render() {

      const startErrorBorder = {
        border: this.state.start_missing ? "1px solid red" : "none",
        borderRadius: "20px",
      };

      const destinationErrorBorder = {
        border: this.state.destination_missing ? "1px solid red" : "none",
        borderRadius: "20px",
      };


      return (
        <div>
          <div>
            <h1>Fahrplanauskunft</h1>
          </div>
          <div>
            <form onSubmit={this.handleSubmit}>
              <div className="formContainer">
                <div>
                  <label htmlFor="start_station">Startbahnhof</label>
                  <div className="inputContainer" style={startErrorBorder}>
                    <input
                      type="text"
                      id="start_station"
                      value={this.state.start_station}
                      onChange={this.handleChange}
                      list="start_stations"
                      placeholder="z.B. Aalen Hbf"
                    />
                    <datalist id="start_stations">
                      {this.startStations.map((station, i) => (
                        <option key={i} value={station} />
                      ))}
                    </datalist>
                  </div>
                </div>
                  <div>
                    <label htmlFor="destination_station">Zielbahnhof</label>
                    <div className="inputContainer"  style={destinationErrorBorder}>
                      <input
                        type="text"
                        id="destination_station"
                        value={this.state.destination_station}
                        onChange={this.handleChange}
                        placeholder="z.B. Ellwangen"
                      />
                    </div>
                </div>

                <div>
                <label htmlFor="time">Uhrzeit</label>
                  <div className="inputContainer">
                    <input
                      type="time"
                      id="time"
                      value={this.state.time}
                      onChange={this.handleChange}
                    />
                  </div>
                </div>
                <div>
                  <label htmlFor="date">Datum</label>
                  <div className="inputContainer">
                    <input
                    type="date"
                      id="date"
                      value={this.state.date}
                      onChange={this.handleChange}
                    />
                  </div>
                </div>
  
                <button className="submitButton" type="submit">Suche</button>
              </div>
            </form>
          </div>

          <br />
          <br />
  
          <div id="results" className="results">
            {/* Results will be displayed here after submitting the form */}
          {this.state.results && this.state.results.start && this.state.results.destination ? (
            <div>
              <h3>{this.state.results.start} - {this.state.results.destination}</h3>
            </div>
          ) : this.state.results && this.state.results.start ? (
            <div>
              <h3>{this.state.results.start}</h3>
            </div>
          ) : (
            null
          )}
          
          <div className="connectionsList">
            {this.state.results && this.state.results.connections ? (
               this.state.results.connections.map((connection, i) => (
              <ConnectionCard
                key={i}
                connection={connection}
                onClick={() => {
                  // Show additional details when clicked
                  console.log('Clicked:', connection);
                }}
              />
            ))) : this.state.results && this.state.results.start && !this.state.results.connection? ( 
              <div>
                No connections
              </div>
            ) : (
              null
            )}
          </div>
        </div>
      </div>
      );
    }
  }
  
  export default Timetable;