INSERT INTO Collision VALUES ();
INSERT INTO Casualty_Class VALUES ();
INSERT INTO Sex VALUES (1, "Male") (2, "Female");
INSERT INTO Age_Band VALUES (7, 36, 45);
INSERT INTO Age_Band_to_Age VALUES (39, 7);
INSERT INTO Pedestrian_Location VALUES ();
INSERT INTO Pedestrian_Movement VALUES ();
INSERT INTO Passenger_location VALUES ();
INSERT INTO Bus_Coach_location VALUES ();
INSERT INTO Maintenance_Worker VALUES ();
INSERT INTO Casualty_Type VALUES ();
INSERT INTO Decile_type VALUES ();
INSERT INTO LSOA VALUES ();
INSERT INTO Casualty_Injury_Based VALUES ();
INSERT INTO Distance_Banding VALUES ();
INSERT INTO Casualty_Severity VALUES ();
INSERT INTO Vehicle VALUES ();

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
    1,              -- vehicle_reference
);
