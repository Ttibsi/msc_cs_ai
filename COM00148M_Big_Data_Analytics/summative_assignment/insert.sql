INSERT INTO Collision VALUES (2024991534042, 2024, '991534042');
INSERT INTO Vehicle_Type VALUES (-1, 'Data missing or out of range');
INSERT INTO Casualty_Class VALUES (3, 'Pedestrian');
INSERT INTO Sex VALUES (2, 'Female');
INSERT INTO Age_Band VALUES (7, 36, 45);
INSERT INTO Age_Band_to_Age VALUES (39, 7);
INSERT INTO Pedestrian_Location VALUES (1, 'Crossing on pedestrian crossing facility');
INSERT INTO Pedestrian_Movement VALUES (3, 'Crossing from driver''s offside');
INSERT INTO Passenger_location VALUES (0, 'Not car passenger');
INSERT INTO Bus_Coach_location VALUES (0, 'Not a bus or coach passenger');
INSERT INTO Maintenance_Worker VALUES (-1, 'Data missing or out of range');
INSERT INTO Casualty_Type VALUES (0, 'Pedestrian');
INSERT INTO Decile_type VALUES (-1, 'Data missing or out of range');
INSERT INTO LSOA VALUES ('-1', -1);
INSERT INTO Casualty_Injury_Based VALUES (1, 'Based on Injury code reporting');
INSERT INTO Distance_Banding VALUES (-1, 'Data missing or out of range');
INSERT INTO Casualty_Severity VALUES (3, 'Slight');
INSERT INTO Vehicle VALUES (2024991534042, 1, -1);


INSERT INTO Casualty VALUES (
    2024991534042,  -- collision_index
    1,              -- casualty_reference
    3,              -- casualty_class
    2,              -- sex_of_casualty
    39,             -- age_of_casualty
    3,              -- enhanced_casualty_severity
    1,              -- pedestrian_location
    3,              -- pedestrian_movement
    0,              -- Passenger_location
    0,              -- Bus_Coach_location
    -1,             -- pedestrian_road_maintenance_worker
    0,              -- casualty_type
    -1,             -- casualty_imd_decile
    -1,             -- lsoa_of_casualty
    1,              -- casualty_injury_based
    0,              -- casualty_adjusted_severity_serious
    1,              -- casualty_adjusted_severity_slight
    -1,             -- distance_band_id 
    3,              -- casualty_severity
    1               -- vehicle_reference
);
