import React from "react";
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import { Spinner } from "react-bootstrap";

import "./prices.css"

import WishPriceTable from "../Components/Table/WishPriceTable";

class Prices extends React.Component {
    constructor(props) {
      super(props);
  
      this.state = {
        start_station: '',
        destination_station: '',
        results: null,
        isLoading: false,
        price_trend_all: null,
        price_increase_all: null,
        budget: null,
        time_slot_start: null,
        time_slot_end: null,
        destination: null,
        wish_price_results: null,
        metrics_start: null,
        metrics_destination: null,
        metrics_results_trends: null,
        metrics_results_increase: null,
        metrics_results_metrics: null,
        metrics_loading: false,
        metrics_sent: false,
        start_missing: false,
        destination_missing: false,
        metrics_start_missing: false,
        metrics_destination_missing: false,
        budget_missing: false,
        price_destination_missing: false,
        time_slot_start_missing: false,
        time_slot_end_missing: false,
      };
    }

    // loads the general price information as soon as the component is mounted
    componentDidMount() {
      this.getPriceTrendAll();
      this.getPriceIncreaseAll();
    }
  
    handleChange = (event) => {
      this.setState({ [event.target.id]: event.target.value });
    };
  
    handleSubmit = async (event) => {
      event.preventDefault();

      // Check if the start station is empty
      if (!this.state.start_station) {
        this.setState({ start_missing: true }); // Set the start_missing state to true if start_station is empty
      } else {
        this.setState({ start_missing: false }); // Set the start_missing state to false if start_station is not empty
      }

      if (!this.state.destination_station) {
        this.setState({ destination_missing: true }); // Set the destination_missing state to true if start_station is empty
      } else {
        this.setState({ destination_missing: false }); // Set the destination_missing state to false if start_station is not empty
      }

      // if any of both are empty we can return instantly
      if (this.state.start_missing || this.state.destination_missing) {
        return;
      }

      this.setState({ isLoading: true })
      // Add your function to send a request with the inputs' content
      const response = await this.sendRequestWithData(
        this.state.start_station,
        this.state.destination_station
      );
  
      // Update the results with the request response
      this.setState({ results: response, isLoading: false });
    };

    handleConnectionSearch = async (event) => {
      event.preventDefault();

      // Check if the start station is empty
      if (!this.state.metrics_start) {
        this.setState({ metrics_start_missing: true }); // Set the metrics_start_missing state to true if start_station is empty
      } else {
        this.setState({ metrics_start_missing: false }); // Set the metrics_start_missing state to false if start_station is not empty
      }

      if (!this.state.metrics_destination) {
        this.setState({ metrics_destination_missing: true }); // Set the metrics_destination_missing state to true if start_station is empty
      } else {
        this.setState({ metrics_destination_missing: false }); // Set the metrics_destination_missing state to false if start_station is not empty
      }

      // if any of both are empty we can return instantly
      if (this.state.start_missing || this.state.destination_missing) {
        return;
      }
      this.setState({ metrics_sent: true })
      this.setState({ metrics_loading: true })
      // Add your function to send a request with the inputs' content
      const response1 = await this.getMetrics(
        this.state.metrics_destination,
      );
      const response2 = await this.getPriceIncrease(
        this.state.metrics_destination,
      );
      const response3 = await this.getPriceTrend(
        this.state.metrics_destination,
      );

      // Update the results with the request response
      this.setState({ metrics_results_metrics: response1, metrics_results_trends: response3, metrics_results_increase: response2, metrics_loading: false });
    };

    getMetrics = async (metrics_destination) => {
      try {
        const response = await fetch('/metrics', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            metrics_destination: metrics_destination,
          }),
        });
    
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
    
        const data = await response.json();
        return data.plot;
      } catch (error) {
        console.error('Error:', error);
        return `Error: ${error.message}`;
      }
    };

    getPriceIncrease = async (metrics_destination) => {
      try {
        const response = await fetch('/increases', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            metrics_destination: metrics_destination,
          }),
        });
    
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
    
        const data = await response.json();
        return data.plot;
      } catch (error) {
        console.error('Error:', error);
        return `Error: ${error.message}`;
      }
    };

    getPriceTrend = async (metrics_destination) => {
      try {
        const response = await fetch('/trends', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            metrics_destination: metrics_destination,
          }),
        });
    
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
    
        const data = await response.json();
        return data.plot;
      } catch (error) {
        console.error('Error:', error);
        return `Error: ${error.message}`;
      }
    };

    handlePriceWish = async (event) => {
      event.preventDefault();

      // Check if the budget is empty
      if (!this.state.budget) {
        this.setState({ budget_missing: true }); // Set the budget_missing state to true if start_station is empty
      } else {
        this.setState({ budget_missing: false }); // Set the budget_missing state to false if start_station is not empty
      }

      // Check if the destination is empty
      if (!this.state.destination) {
        this.setState({ price_destination_missing: true }); // Set the price_destination_missing state to true if start_station is empty
      } else {
        this.setState({ price_destination_missing: false }); // Set the price_destination_missing state to false if start_station is not empty
      }

      // Check if the start intervall is empty
      if (!this.state.time_slot_start) {
        this.setState({ time_slot_start_missing: true }); // Set the time_slot_start_missing state to true if start_station is empty
      } else {
        this.setState({ time_slot_start_missing: false }); // Set the time_slot_start_missing state to false if start_station is not empty
      }

      // Check if the end intervall is empty
      if (!this.state.time_slot_end ) {
        this.setState({ time_slot_end_missing: true }); // Set the time_slot_end_missing state to true if start_station is empty
      } else {
        this.setState({ time_slot_end_missing: false }); // Set the time_slot_end_missing state to false if start_station is not empty
      }

      // if any of both are empty we can return instantly
      if (this.state.budget_missing || this.state.price_destination_missing || this.state.time_slot_start_missing || this.state.time_slot_end_missing) {
        return;
      }

      this.setState({ isLoading: true })
      // Add your function to send a request with the inputs' content
      const response = await this.getWishPrice(
        this.state.budget,
        this.state.time_slot_start,
        this.state.time_slot_end,
        this.state.destination,
      );
  
      // Update the results with the request response
      this.setState({ wish_price_results: response, isLoading: false });
    };

    getWishPrice = async (budget, time_slot_start, time_slot_end, destination) => {
      try {
        const response = await fetch('/price_wish', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            budget: budget,
            time_slot_start: time_slot_start,
            time_slot_end: time_slot_end,
            destination: destination,
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

    getPriceTrendAll = async () => {
      try {
        const response = await fetch('/price_trend_all', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
    
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
    
        const data = await response.json();
        this.setState({ price_trend_all: data.plot }); // Update the state with the plot image
      } catch (error) {
        console.error("Error:", error);
        this.setState({ price_trend_all: `Error: ${error.message}` });
      }
    };

    getPriceIncreaseAll = async () => {
      try {
        const response = await fetch('/price_increase_all', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
    
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
    
        const data = await response.json();
        this.setState({ price_increase_all: data.plot }); // Update the state with the plot image
      } catch (error) {
        console.error("Error:", error);
        this.setState({ price_increase_all: `Error: ${error.message}` });
      }
    };

    sendRequestWithData = async (start_station, destination_station) => {
      try {
        const response = await fetch('/prices_submit', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            start_station: start_station,
            destination_station: destination_station,
          }),
        });
    
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
    
        const data = await response.json();
        return data.plot;
      } catch (error) {
        console.error('Error:', error);
        return `Error: ${error.message}`;
      }
    };
  
    render() {

      const { price_trend_all } = this.state;
      const { price_increase_all } = this.state;

      // error styles for web crawler
      const startErrorBorder = {
        border: this.state.start_missing ? "1px solid red" : "none",
        borderRadius: "20px",
      };

      const destinationErrorBorder = {
        border: this.state.destination_missing ? "1px solid red" : "none",
        borderRadius: "20px",
      };

      // error styles for connection search
      const metricsStartErrorBorder = {
        border: this.state.metrics_start_missing ? "1px solid red" : "none",
        borderRadius: "20px",
      };

      const metricsDestinationErrorBorder = {
        border: this.state.metrics_destination_missing ? "1px solid red" : "none",
        borderRadius: "20px",
      };

      // error styles for wish price
      const budgetErrorBorder = {
        border: this.state.budget_missing ? "1px solid red" : "none",
        borderRadius: "20px",
      };

      const destinationPriceErrorBorder = {
        border: this.state.price_destination_missing ? "1px solid red" : "none",
        borderRadius: "20px",
      };

      const startIntervalErrorBorder = {
        border: this.state.time_slot_start_missing ? "1px solid red" : "none",
        borderRadius: "20px",
      };

      const endIntervalErrorBorder = {
        border: this.state.time_slot_end_missing ? "1px solid red" : "none",
        borderRadius: "20px",
      };

      return (
        <div>
          <div>
            <h1>Preisanalyse</h1>
          </div>
            <Tabs
              defaultActiveKey="general"
              className="mb-3"
            >
              <Tab eventKey="general" title="Allgemein">
                <Tabs defaultActiveKey="price_trend" className="mb-3">
                  <Tab eventKey="price_trend" title="Preisverlauf Tage & Wochen">
                    <div className="results">
                      {price_trend_all && price_trend_all.startsWith("Error") ? (
                        <p>{price_trend_all}</p>
                      ) : price_trend_all ? (
                        <img className="result_image"
                          src={`data:image/png;base64,${price_trend_all}`}
                          alt="Price trend plot"
                        />
                      ) : (
                        <Spinner animation="border" role="status">
                          <span className="visually-hidden">Loading...</span>
                        </Spinner>
                      )}
                    </div>
                  </Tab>
                  <Tab eventKey="price_increase" title="Preisverlauf Tageszeit">
                    <div className="results">
                      {price_increase_all && price_increase_all.startsWith("Error") ? (
                        <p>{price_increase_all}</p>
                      ) : price_increase_all ? (
                        <img className="result_image"
                          src={`data:image/png;base64,${price_increase_all}`}
                          alt="Price increase plot"
                        />
                      ) : (
                        <Spinner animation="border" role="status">
                          <span className="visually-hidden">Loading...</span>
                        </Spinner>
                      )}
                    </div>
                  </Tab>
                </Tabs>
              </Tab>
              <Tab eventKey="specific_connection" title="Verbindungssuche">
                <div>
                  <form onSubmit={this.handleConnectionSearch}>
                  <div className="formContainer">
                    <div>
                      <label htmlFor="metrics_start">Startbahnhof</label>
                      <div className="inputContainer" style={metricsStartErrorBorder}>
                        <input
                          type="text"
                          id="metrics_start"
                          value={this.state.metrics_start}
                          onChange={this.handleChange}
                          placeholder="z.B. Aalen Hbf"
                        />
                      </div>
                    </div>
                    <div>
                      <label htmlFor="metrics_destination">Zielbahnhof</label>
                      <div className="inputContainer" style={metricsDestinationErrorBorder}>
                        <input
                          type="text"
                          id="metrics_destination"
                          value={this.state.metrics_destination}
                          onChange={this.handleChange}
                          placeholder="z.B. München Hbf"
                        />
                      </div>
                    </div>
      
                    <button className="submitButton" type="submit">OK</button>
                  </div>
                </form>
              </div>
      
              <br />
              <br />

              {this.state.metrics_sent ? (
                <Tabs defaultActiveKey="price_trend_plot" className="mb-3">
                  <Tab eventKey="price_trend_plot" title="Preisverlauf Tage & Wochen">
                    <div className="results">
                      {this.state.metrics_results_trends && this.state.metrics_results_trends.startsWith("Error") ? (
                        <p>{this.state.metrics_results_trends}</p>
                      ) : this.state.metrics_results_trends ? (
                        
                          <img className="result_image"
                            src={`data:image/png;base64,${this.state.metrics_results_trends}`}
                            alt="Price trend plot"
                          />
                        
                        ) : this.state.metrics_loading ? (
                          <Spinner animation="border" role="status">
                            <span className="visually-hidden">Loading...</span>
                          </Spinner>
                        ) : (
                          null
                        )}
                    </div>
                  </Tab>
                  <Tab eventKey="price_increase_plot" title="Preisverlauf Tageszeit">
                    <div className="results">
                      {this.state.metrics_results_increase && this.state.metrics_results_increase.startsWith("Error") ? (
                        <p>{this.state.metrics_results_increase}</p>
                      ) : this.state.metrics_results_increase ? (
                        
                          <img className="result_image"
                            src={`data:image/png;base64,${this.state.metrics_results_increase}`}
                            alt="Price increase plot"
                          />
                        
                      ) : (
                        null
                      )}
                    </div>
                  </Tab>
                  <Tab eventKey="price_metrics_plot" title="Preis Metriken">
                    <div className="results">
                      {this.state.metrics_results_metrics && this.state.metrics_results_metrics.startsWith("Error") ? (
                        <p>{this.state.metrics_results_metrics}</p>
                      ) : this.state.metrics_results_metrics ? (
                        
                          <img className="result_image"
                            src={`data:image/png;base64,${this.state.metrics_results_metrics}`}
                            alt="Price increase plot"
                          />
                        
                      ) : (
                        null
                      )}
                    </div>
                  </Tab>
                </Tabs>
              ) : ( 
                null
                )}

              </Tab>
              <Tab eventKey="wish_price" title="Wunschpreis">
              <div>
                  <form onSubmit={this.handlePriceWish}>
                  <div className="formContainer">
                    <div>
                      <label htmlFor="budget">Budget in Euro</label>
                      <div className="inputContainer"  style={budgetErrorBorder}>
                        <input
                          type="number"
                          id="budget"
                          value={this.state.budget}
                          onChange={this.handleChange}
                          placeholder="43"
                          min={0}
                        />
                      </div>
                    </div>
                    <div>
                      <label htmlFor="destination">Zielbahnhof</label>
                      <div className="inputContainer"  style={destinationPriceErrorBorder}>
                        <input
                          type="text"
                          id="destination"
                          value={this.state.destination}
                          onChange={this.handleChange}
                          placeholder="z.B. München Hbf"
                        />
                      </div>
                    </div>
                    <div>
                      <label htmlFor="time_slot_start">Startuhrzeit</label>
                      <div className="inputContainer"  style={startIntervalErrorBorder}>
                        <input
                          type="number"
                          id="time_slot_start"
                          value={this.state.time_slot_start}
                          onChange={this.handleChange}
                          placeholder="9"
                          min={0}
                          max={24}
                        />
                      </div>
                    </div>
                    <div>
                      <label htmlFor="time_slot_end">Enduhrzeit</label>
                      <div className="inputContainer"  style={endIntervalErrorBorder}>
                        <input
                          type="number"
                          id="time_slot_end"
                          value={this.state.time_slot_end}
                          onChange={this.handleChange}
                          placeholder="14"
                          min={0}
                          max={24}
                        />
                      </div>
                    </div>
      
                    <button className="submitButton" type="submit">OK</button>
                  </div>
                </form>
              </div>
      
              <br />
              <br />

              <div className="wish-price-result">
                {this.state.wish_price_results ? (
                  <div>
                    <WishPriceTable data={this.state.wish_price_results}/>
                  </div>
                ) : this.state.isLoading ? (
                  <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </Spinner>
                ) : (
                  null
                )}
              </div>
              </Tab>
              <Tab eventKey="web_crawl_price" title="Aktuelle Preissuche">
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
                          placeholder="z.B. Aalen Hbf"
                        />
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
                          placeholder="z.B. München Hbf"
                        />
                      </div>
                    </div>
      
                    <button className="submitButton" type="submit">OK</button>
                  </div>
                </form>
              </div>
      
              <br />
              <br />

              <div className="results">
                {this.state.results && this.state.results.startsWith("Error") ? (
                  <p>{this.state.results}</p>
                ) : this.state.results ? (
                  <img className="result_image"
                    src={`data:image/png;base64,${this.state.results}`}
                    alt="Web Crawl plot"
                  />
                ) : this.state.isLoading ? (
                  <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </Spinner>
                ) : (
                  null
                )}
              </div>
              </Tab>
            </Tabs>
        </div>
      );
    }
  }

export default Prices;