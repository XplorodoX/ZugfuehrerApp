import React from 'react';
import { Link } from 'react-router-dom';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Nav from 'react-bootstrap/Nav';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';

import logoImage from '../Images/logo.png'

import "./main.css"
import Timetable from './timetable';
import Delays from './delays';
import Prices from './prices';



class Main extends React.Component {
  render() {
    return (
      // creates the general site layout with the different tabs on the left side to navigate the pages
      <div className="min-vh-100" style={{ overflow: 'hidden' }}>
      <Tab.Container defaultActiveKey="timetable" className="min-vh-100">
        <Row className="min-vh-100" noGutters>
          <Col sm={2} className="navCol min-vh-100 no-margin-padding">
            <Nav className="flex-column text-center d-flex navContainer">
            <Nav.Item className="navLogo">
                <Nav.Link as={Link} to="/" className="d-flex align-items-center">
                    <img src={logoImage} alt="Logo" />
                </Nav.Link>
            </Nav.Item>
            <Nav.Item className='navTab'>
              <Nav.Link eventKey="timetable">Fahrplanauskunft</Nav.Link>
            </Nav.Item>
            <Nav.Item className='navTab'>
              <Nav.Link eventKey="delays">Verspätungsanalyse</Nav.Link>
            </Nav.Item>
            <Nav.Item className='navTab'>
              <Nav.Link eventKey="prices">Preisanalyse</Nav.Link>
            </Nav.Item>
          </Nav>
        </Col>
        <Col className='contentCol min-vh-100'>
          <Tab.Content className='contentContainer'>
            <Tab.Pane eventKey="timetable">
                <Timetable />
            </Tab.Pane>
            <Tab.Pane eventKey="delays">
                <Delays />
            </Tab.Pane>
            <Tab.Pane eventKey="prices">
                <Prices />
            </Tab.Pane>
          </Tab.Content>
        </Col>
      </Row>
      </Tab.Container>
    </div>
    );
  }
}

export default Main;