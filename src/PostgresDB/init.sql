ALTER ROLE postgres SET client_min_messages = WARNING;

CREATE TABLE trainstation (
  trainstation_id int PRIMARY KEY,
  name TEXT NOT NULL
);

INSERT INTO trainstation (trainstation_id, name) VALUES (8000002, 'Aalen hbf');
INSERT INTO trainstation (trainstation_id, name) VALUES (8000329, 'Schwäbisch Gmünd');
INSERT INTO trainstation (trainstation_id, name) VALUES (8002689, 'Heidenheim');
INSERT INTO trainstation (trainstation_id, name) VALUES (8003525, 'Langenau(Württ)');
INSERT INTO trainstation (trainstation_id, name) VALUES (8000170, 'Ulm Hbf');
INSERT INTO trainstation (trainstation_id, name) VALUES (8005424, 'Schorndorf');
INSERT INTO trainstation (trainstation_id, name) VALUES (8000096, 'Stuttgart Hbf');
INSERT INTO trainstation (trainstation_id, name) VALUES (8000284, 'Nürnberg Hbf');
INSERT INTO trainstation (trainstation_id, name) VALUES (8001751, 'Ellwangen');
INSERT INTO trainstation (trainstation_id, name) VALUES (784839, 'Donauwörth');
INSERT INTO trainstation (trainstation_id, name) VALUES (8000180, 'Waiblingen');
INSERT INTO trainstation (trainstation_id, name) VALUES (8000067, 'Crailsheim');
INSERT INTO trainstation (trainstation_id, name) VALUES (8000191, 'Karlsruhe Hbf');
INSERT INTO trainstation (trainstation_id, name) VALUES (8000299, 'Pforzheim Hbf');
INSERT INTO trainstation (trainstation_id, name) VALUES (8000280, 'Nördlingen');
INSERT INTO trainstation (trainstation_id, name) VALUES (8004549, 'Oberkochen');
INSERT INTO trainstation (trainstation_id, name) VALUES (8000261, 'München Hbf');
INSERT INTO trainstation (trainstation_id, name) VALUES (8000013, 'Augsburg Hbf');

CREATE TABLE timetable (
    timetable_id TEXT PRIMARY KEY,
    trainstation_id INT NOT NULL,
    date DATE,
    name TEXT,
    arrival_time TIME,
    departure_time TIME,
    platform INT,
    train_number INT not null,
    train_type TEXT,
    destination TEXT,
    FOREIGN KEY (trainstation_id) REFERENCES trainstation (trainstation_id)
);

CREATE TABLE changestimetable (
    timetable_id_new TEXT PRIMARY KEY,
    new_arrival_time TIME,
    new_departure_time TIME,
    new_platform INT,
    FOREIGN KEY (timetable_id_new) REFERENCES timetable (timetable_id)
);