// Author: Marc Nebel
// Beschreibung: Frontend für das Nutzen der Verspätungsdaten. Aufgrund von Zeitmangel leider vollständig unfertig. 

import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import './delays.css';

const DelayPage = () => {
  const [data, setData] = useState([]);
  const [lineID, setLineID] = useState('');
  const [station, setStation] = useState('');
  const [t_station, setTStation] = useState('');
  const [time, setTime] = useState(null);
  const [selectedRow, setSelectedRow] = useState(null);
  const [error, setError] = useState(null);
  const [subData, setSubData] = useState([]);
  const [plotData, setPlotData] = useState([]);
  const [activeButton, setActiveButton] = useState('');
  const [subData2, setSubData2] = useState([]);
  const [subData3, setSubData3] = useState([]);


  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    fetchSubData();
    fetchPlotData();
  }, [selectedRow, activeButton]);

  const fetchData = async () => {
    try {
      let url = 'http://localhost:5005/delay/';

      if (lineID) {
        url += `n/${lineID}`;
      }
      if (station) {
        url += `station/${station}`;
      }
      if (t_station) {
        url += `destination/${t_station}`;
      }
      if (time) {
        const hour = parseInt(time.split(':')[0], 10);
        url += `time/${hour}`;
      }

      const response = await fetch(url);
      const jsonData = await response.json();
      setData(jsonData);
      setError(null);
    } catch (error) {
      console.log('Error fetching data:', error);
      setError('Error fetching data');
    }
  };

  const fetchSubData = async () => {
    if (selectedRow !== null) {
      try {
        const item = data[selectedRow];
        const date = new Date(item.date).toISOString().split('T')[0];
        const endpoint1 = `http://localhost:5005/delay/n/${item.n}/date/${date}`;
        const endpoint2 = `http://localhost:5005/avg_delay_at_final/n/${item.n}`;
        const endpoint3 = `http://localhost:5005/avg_delay_destination_final/destination/${item.destination}`;
  
        const response1 = await fetch(endpoint1);
        const jsonData1 = await response1.json();
        setSubData(jsonData1);
  
        const response2 = await fetch(endpoint2);
        const jsonData2 = await response2.json();
        setSubData2(jsonData2);
  
        const response3 = await fetch(endpoint3);
        const jsonData3 = await response3.json();
        setSubData3(jsonData3);
      } catch (error) {
        console.log('Error fetching sub data:', error);
      }
    } else {
      setSubData([]);
      setSubData2([]);
      setSubData3([]);
    }
  };
  

  const fetchPlotData = async () => {
    if (selectedRow !== null) {
      try {
        const item = data[selectedRow];
        const date = new Date(item.date).toISOString().split('T')[0];
        let endpoint = '';
        let plotType = '';
        let color = '';

        switch (activeButton) {
          case 'Button 1':
            endpoint = `http://localhost:5005/avg_delay_at/n/${item.n}`;
            plotType = 'line';
            color = 'red';
            break;
          case 'Button 2':
            endpoint = `http://localhost:5005/endpoint2/n/${item.n}/date/${date}`;
            plotType = 'bar';
            break;
          case 'Button 3':
            endpoint = `http://localhost:5005/endpoint3/n/${item.n}/date/${date}`;
            plotType = 'bar';
            break;
          default:
            endpoint = `http://localhost:5005/delay/n/${item.n}/date/${date}`;
            plotType = 'line';
            color = 'blue';
            break;
        }

        const response = await fetch(endpoint);
        const jsonData = await response.json();

        const xValues = jsonData.map((entry) => entry.station);
        const yValues = jsonData.map((entry) => entry.ar_time_diff);

        const subtablePlotData = {
          x: xValues,
          y: yValues,
          mode: 'lines+markers',
          type: plotType,
          line: {
            color: color,
          },
        };

        setPlotData(subtablePlotData);
      } catch (error) {
        console.log('Error fetching plot data:', error);
      }
    } else {
      setPlotData([]);
    }
  };

  const handleRowClick = (index) => {
    setSelectedRow((prevSelectedRow) => {
      if (prevSelectedRow === index) {
        return index;
      }
      setActiveButton('');
      return index;
    });
  };
  
  const handleButtonClick = (buttonName) => {
    setActiveButton(buttonName);
  };
  

  const formatDateTime = (time) => {
    const date = new Date(time);
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  };
 

  const formatDateTimeDelay = (time) => {
    const timeParts = time.split(' ');
    const [days, hms] = timeParts.slice(1);
    const [hours, minutes] = hms.split(':');
    return `${hours}:${minutes}`;
  };

  return (
    <div>
      <h1>Delay Page</h1>

      {/* Text fields and button */}
      <div>
        <input
          type="text"
          placeholder="LineID"
          value={lineID}
          onChange={(e) => setLineID(e.target.value)}
        />
        <input
          type="text"
          placeholder="Station"
          value={station}
          onChange={(e) => setStation(e.target.value)}
        />
        <input
          type="text"
          placeholder="Target Station"
          value={t_station}
          onChange={(e) => setTStation(e.target.value)}
        />
        <input
          type="time"
          value={time}
          onChange={(e) => setTime(e.target.value)}
        />
        <button onClick={fetchData}>Filter</button>
      </div>

      {/* Error message */}
      {error && <div className="error-message">{error}</div>}

      {/* Delay list */}
      <div className="cards-container">
        {Array.isArray(data) &&
          data.map((item, index) => (
            !item.final_station && (
              <div
                key={index}
                className={`card ${index === selectedRow ? 'active' : ''}`}
                onClick={() => handleRowClick(index)}
              >
                <div className="card-content">
                  <strong>Datum:</strong> {formatDateTime(item.date)}
                  <br />
                  <strong>{item.first_station ? 'Startbahnhof:' : 'Von:'}</strong> {item.station}
                  <br />
                  <strong>Endbahnhof:</strong> {item.final_station ? item.station : item.destination}
                  <br />
                </div>
                {index === selectedRow && (
                  <div className="expanded-content">
                    <strong>Heutige Ankunftsverspätung:</strong> {formatDateTimeDelay(item.ar_time_diff)}
                    <br />
                    <strong>Heutige Abfahrtsverspätung:</strong> {formatDateTimeDelay(item.dp_time_diff)}
                    <br />

                    <div className="plot-section">
                      {/* Add the Plot component */}
                      <div className="plot-container">
                        <Plot
                          data={[plotData]}
                          layout={{ width: 400, height: 300, title: 'Line Chart' }} 
                        />
                      </div>

                      {/* Add the buttons */}
                      <div className="buttons-container">
                        <button
                          className={activeButton === 'Button 1' ? 'active' : ''}
                          onClick={() => handleButtonClick('Button 1')}
                        >
                          Button 1
                        </button>
                        <button
                          className={activeButton === 'Button 2' ? 'active' : ''}
                          onClick={() => handleButtonClick('Button 2')}
                        >
                          Button 2
                        </button>
                        <button
                          className={activeButton === 'Button 3' ? 'active' : ''}
                          onClick={() => handleButtonClick('Button 3')}
                        >
                          Button 3
                        </button>
                      </div>
                    </div>

                    {/* Subtable */}
                    {Array.isArray(subData) && (
                      <table>
                        <thead>
                          <tr>
                            <th>Bahnhöfe auf der Route</th>
                            <th>Heutige Ankunftsverspätung</th>
                            <th>Heutige Abfahrtsverspätung</th>
                          </tr>
                        </thead>
                        <tbody>
                          {subData.map((subItem, subIndex) => (
                            <tr key={subIndex}>
                              <td>{subItem.station}</td>
                              <td>{formatDateTimeDelay(subItem.ar_time_diff)}</td>
                              <td>{formatDateTimeDelay(subItem.dp_time_diff)}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                    {Array.isArray(subData2) && (
                      <table>
                        <thead>
                          <tr>
                            <th>Durchschnitliche Verspätung am Ende der Verbindung</th>
                            <th>Durchschnitliche Verspätung am Anfang der Verbindung</th>
                          </tr>
                        </thead>
                        <tbody>
                          {subData2.map((subItem, subIndex) => (
                            <tr key={subIndex}>
                              <td>{subItem.ar_time_diff}</td>
                              <td>{subItem.dp_time_diff}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                    {Array.isArray(subData3) && (
                      <table>
                        <thead>
                          <tr>
                            <th>Durchschnitliche Verspätung am Zielbahnhof für alle Verbindungen</th>
                            <th>Durchschnitliche Verspätung am Startbahnhof für alle Verbindungen</th>
                          </tr>
                        </thead>
                        <tbody>
                          {subData3.map((subItem, subIndex) => (
                            <tr key={subIndex}>
                              <td>{subItem.ar_time_diff}</td>
                              <td>{subItem.dp_time_diff}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                  </div>
                )}
              </div>
            )
          ))}
      </div>
    </div>
  );
};

export default DelayPage;
