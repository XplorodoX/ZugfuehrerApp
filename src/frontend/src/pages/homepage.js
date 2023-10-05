import React from "react";
import { Link } from 'react-router-dom';
import { Container, Card, Row, Col } from "react-bootstrap";
import "./homepage.css";

const Homepage = () => {
    return (
        <div className="homepage">
            <div className="section-1">
                {/* Heading at the top center */}
                <h1>
                    <span className="save-text">SAVE</span>
                    <span className="money-text">TIME<br/>& MONEY</span>
                </h1>

                <div className="spacer"></div>

                <Link to="/main">
                    <button className="custom-button">Start now!</button>
                </Link>
                
                {/* Bouncing arrow */}
                <div className="bouncing-arrow">
                    {/* Add your bouncing arrow icon or image here */}
                </div>
            </div>
            
            <div className="section-2">
                {/* About us content */}
                <Container fluid className="jumbotron-container" style={ { paddingBottom: "0rem" } }>
                    <Container style={ { maxWidth: "60%", display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', marginBottom: "2rem" } }>
                        <h1>Train Guide - Über uns</h1>
                        <p>Willkommen zum Train Guide, der unverzichtbaren Anwendung, die für effiziente, kostengünstige und umweltfreundlichere Reisen mit der Deutschen Bahn entwickelt wurde. Diese Anwendung wurde von vier Studenten der Data Science erstellt, um dir das bestmögliche Zugreiseerlebnis zu bieten.</p>
                    </Container>
                    <Container style= {{ marginBottom: "3rem" }}>
                        <Row>
                            <Col sm={4}>
                                <Card className="info-card" style={ { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'} }>
                                    <Card.Header as="h2">Alles an einem Ort</Card.Header>
                                    <Card.Body>
                                        <Card.Text>
                                            Egal ob du nach aktuellen Fahrplänen mit Live-Verspätungen, Verspätungsanalysen oder Preisanalysen des Fernverkehrs suchst, der Train Guide liefert all das für dich.
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            </Col>
                            <Col sm={4}>
                                <Card className="info-card" style={ { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' } }>
                                    <Card.Header as="h2">Spare Geld & Zeit</Card.Header>
                                    <Card.Body>
                                        <Card.Text>
                                        Möchtest du Geld sparen? Der Train Guide zeigt dir, wann und wie die Preise für Fernreisen typischerweise ansteigen, und hilft dir, den besten Zeitpunkt zum Buchen deines Tickets zu ermitteln. 
                                        </Card.Text>
                                    </Card.Body>
                                    </Card>
                                </Col>
                            <Col sm={4}>
                                <Card className="info-card" style={ { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' } }>
                                    <Card.Header as="h2">Dein Beitrag zum Klimaschutz</Card.Header>
                                    <Card.Body>
                                        <Card.Text>
                                        Der Train Guide trägt dazu bei, die Straßen leerer zu machen und CO2-Emissionen zu reduzieren. Je mehr wir Bahn fahren und je effizienter wir unsere Reisen planen, desto mehr tun wir für unsere Umwelt.
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            </Col>
                        </Row>
                    </Container>
                    <Container className="bottom-text" style={ { maxWidth: "60%", display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' } }>
                        <p>Wir sind vier Data Science Studenten und haben im Rahmen des Fachs Cloud & Distributed Computing dieses Projekt geplant und entwickelt. Wir haben uns zum Ziel gemacht, die Daten der Deutschen Bahn in verständliche und nützliche Informationen für dich umzuwandeln. Wir arbeiten ständig daran, die Genauigkeit unserer Daten und Vorhersagen zu verbessern, um dir das bestmögliche Reiseerlebnis zu bieten.</p>
                        <p>Wir hoffen, dass dir der Train Guide bei deinen Reisen mit der Deutschen Bahn hilft und wünschen dir eine angenehme und effiziente Fahrt!</p> <br></br>
                        <p style={{ fontSize: "14px" }}>Bitte beachte, dass die angezeigten Informationen auf den verfügbaren Daten basieren und möglicherweise nicht in Echtzeit aktualisiert werden. Die Deutsche Bahn ist für die Genauigkeit und Aktualität der Daten verantwortlich.</p> <br></br>
                    </Container>
                    </Container>
                <div style={{ fontSize: "12px" }}>
                    <p>
                        Die Daten werden bereitgestellt von der <a href="https://developers.deutschebahn.com/db-api-marketplace/apis/" title="DB Station&Service AG">DB Station&Service AG</a> <br></br>
                        Logo generated by <a href="https://www.designevo.com/" title="Free Online Logo Maker">DesignEvo free logo designer</a></p>
                </div>
            </div>
        </div>
    )
}

export default Homepage;