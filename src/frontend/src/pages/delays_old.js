import React from "react";
import "./delays.css"
import DelaysTable from '../Components/Table/DelaysTable';
import Plot from 'react-plotly.js';

class Delays extends React.Component {
    constructor(props) {
      super(props);
  
      this.state = {
        line_id: '',
        datetime: '',
        results: [],
        results_sub: [],
      };
    }
  
    handleChange = (event) => {
      this.setState({ [event.target.id]: event.target.value });
    };
  
    handleSubmit = async (event) => {
      event.preventDefault();
  
      // Add your function to send a request with the inputs' content
      const response = await this.sendRequestWithData(
        this.state.line_id,
        this.state.datetime
      );
  
      // Update the results with the request response
      this.setState({ results: response });
    };
  
    sendRequestWithData = async (line_id, datetime) => {
      // Implement your request logic here, using fetch() or other libraries like Axios to send the request
      // and include the input values.
      try {
        const response = await fetch('/delays_submit', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            line_id: line_id,
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
        return `Error: ${error.message}`;
      }
    };

    getPlotConfig() {
      const { results } = this.state;
      
      
      const data = [
        {
          x: results.map((result) => result.n),
          y: results.map((result) => result.dp_time_diff),
          type: 'scatter',
        },
      ];
  
      const layout = {
        title: 'My Plot',
        xaxis: { title: 'X-axis' },
        yaxis: { title: 'Y-axis' },
      };
  
      return { data, layout };
    }

    render() {
      const { data: plot_data, layout } = this.getPlotConfig();
      return (
        <div>
          <div>
            <h1>Verspätungsanalyse</h1>
          </div>
          <div>
            <form onSubmit={this.handleSubmit}>
              <div className="formContainer">
                <div>
                  <label htmlFor="line_id">Verbindungs ID</label>
                  <input
                    type="text"
                    id="line_id"
                    value={this.state.line_id}
                    onChange={this.handleChange}
                  />
                </div>
  
                <div>
                  <label htmlFor="datetime">Datum & Uhrzeit</label>
                  <input
                    type="datetime-local"
                    id="datetime"
                    value={this.state.datetime}
                    onChange={this.handleChange}
                  />
                </div>
  
                <button type="submit">OK</button>
              </div>
            </form>
          </div>
  
          <br />
          <br />
  
          <div className="results-container">
          <div className="table-container">
            {this.state.results && <DelaysTable data={this.state.results} />}
          </div>
          <div className="plot-container">
            <Plot data={plot_data} layout={layout} />
          </div>
        </div>
      </div>
      );
    }
  }

export default Delays;