// Importing modules
import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Homepage from "./pages/homepage";
import Timetable from "./pages/timetable";
import Prices from "./pages/prices";
import Delays from "./pages/delays";
import Main from "./pages/main";

function App() {
	// usestate for setting a javascript
	// object for storing and using data
	const [data, setdata] = useState({
		timetable_id: "",
	});

	// Using useEffect for single rendering
	useEffect(() => {
		// Using fetch to fetch the api from
		// flask server it will be redirected to proxy
		fetch("/test").then((res) =>
			res.json().then((data) => {
				// Setting a data from api
				setdata({
					timetable_id: data._id,
				});
			})
		);
	}, []);

	return (
		<Router>
			<Routes>
				<Route exact path="/" element={<Homepage />} />
				<Route path="/timetable" element={<Timetable />} />
				<Route path="/prices" element={<Prices />} />
				<Route path="/delays" element={<Delays />} />
				<Route path="/main" element={<Main />} />
			</Routes>
		</Router>
	);
}

export default App;
