INSERT INTO Age_Band VALUES (7, 36, 45);
INSERT INTO Age_Band_to_Age VALUES (39, 7);

INSERT INTO Casualty_Sex VALUES (2, 'Female');
INSERT INTO Casualty_Severity VALUES (3, 'Slight');
INSERT INTO Enhanced_Casualty_Severity VALUES (3, 'Slight');

INSERT INTO Passenger_location VALUES (0, 'Not car passenger');
INSERT INTO Bus_Coach_location VALUES (0, 'Not a bus or coach passenger');
INSERT INTO Distance_Banding VALUES (-1, 'Data missing or out of range');

INSERT INTO Maintenance_Worker VALUES (-1, 'Data missing or out of range');
INSERT INTO Pedestrian_Location VALUES (1, 'Crossing on pedestrian crossing facility');
INSERT INTO Pedestrian_Movement VALUES (3, 'Crossing from driver''s offside');
INSERT INTO Casualty_Type VALUES (0, 'Pedestrian');
INSERT INTO Casualty_Class VALUES (3, 'Pedestrian');

INSERT INTO Pedestrian VALUES (
    1,
    1,
    3,
    -1
);

INSERT INTO LSOA VALUES (
    1,
    -1,
    '-1'
);

INSERT INTO Casualty VALUES (
    1,
    3,
    2,
    39,
    3,
    1,
    0,
    0,
    0,
    1,
    3,
    -1
);

INSERT INTO Vehicle VALUES (1);

INSERT INTO Casualties_In_Collision VALUES (
    2024991534042,
    1,
    1
);

INSERT INTO Collision VALUES (
    2024,
    991534042,
    2024991534042
);
