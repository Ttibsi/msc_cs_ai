CREATE TABLE Age_Band (
    age_band_id INTEGER PRIMARY KEY,
    min_age INTEGER,
    max_age INTEGER
);

CREATE TABLE Age_Band_to_Age (
    age INTEGER PRIMARY KEY,
    age_band_id INTEGER,
    FOREIGN KEY (age_band_id) REFERENCES Age_Band(age_band_id)
);

CREATE TABLE Casualty_Sex (
    sex_of_casualty INTEGER PRIMARY KEY,
    description TEXT
);

CREATE TABLE Casualty_Severity (
    casualty_severity_id INTEGER PRIMARY KEY,
    description TEXT
);

CREATE TABLE Enhanced_Casualty_Severity (
    enhanced_casualty_severity INTEGER PRIMARY KEY,
    description TEXT
);

CREATE TABLE Passenger_location (
    car_passenger INTEGER PRIMARY KEY,
    description TEXT
);

CREATE TABLE Bus_Coach_location (
    bus_or_coach_passenger INTEGER PRIMARY KEY,
    description TEXT
);

CREATE TABLE Distance_Banding (
    distance_band_id INTEGER PRIMARY KEY,
    description TEXT
);

CREATE TABLE Maintenance_Worker (
    pedestrian_road_maintenance_worker_id INTEGER PRIMARY KEY,
    description TEXT
);

CREATE TABLE Pedestrian_Location (
    pedestrian_location INTEGER PRIMARY KEY,
    description TEXT
);

CREATE TABLE Pedestrian_Movement (
    pedestrian_movement INTEGER PRIMARY KEY,
    description TEXT
);

CREATE TABLE Casualty_Type (
    casualty_type INTEGER PRIMARY KEY,
    description TEXT
);

CREATE TABLE Pedestrian (
    pedestrian_id INTEGER PRIMARY KEY,
    pedestrian_location INTEGER,
    pedestrian_movement INTEGER,
    pedestrian_road_maintenance_worker_id INTEGER,
    FOREIGN KEY (pedestrian_location) REFERENCES Pedestrian_Location(pedestrian_location),
    FOREIGN KEY (pedestrian_movement) REFERENCES Pedestrian_Movement(pedestrian_movement),
    FOREIGN KEY (pedestrian_road_maintenance_worker_id) REFERENCES Maintenance_Worker(pedestrian_road_maintenance_worker_id)
);

CREATE TABLE LSOA (
    LSOA_id INTEGER PRIMARY KEY,
    casualty_imd_decile INTEGER,
    lsoa_of_casualty TEXT
);

CREATE TABLE Casualty (
    casualty_reference INTEGER PRIMARY KEY,
    casualty_class INTEGER,
    sex_of_casualty INTEGER,
    age_of_casualty INTEGER,
    casualty_severity INTEGER,
    pedestrian_id INTEGER,
    car_passenger INTEGER,
    bus_or_coach_passenger INTEGER,
    casualty_type INTEGER,
    LSOA_id INTEGER,
    enhanced_casualty_severity INTEGER,
    casualty_distance_banding INTEGER,
    FOREIGN KEY (sex_of_casualty) REFERENCES Casualty_Sex(sex_of_casualty),
    FOREIGN KEY (age_of_casualty) REFERENCES Age_Band_to_Age(age),
    FOREIGN KEY (casualty_severity) REFERENCES Casualty_Severity(casualty_severity_id),
    FOREIGN KEY (pedestrian_id) REFERENCES Pedestrian(pedestrian_id),
    FOREIGN KEY (car_passenger) REFERENCES Passenger_location(car_passenger),
    FOREIGN KEY (bus_or_coach_passenger) REFERENCES Bus_Coach_location(bus_or_coach_passenger),
    FOREIGN KEY (casualty_type) REFERENCES Casualty_Type(casualty_type),
    FOREIGN KEY (LSOA_id) REFERENCES LSOA(LSOA_id),
    FOREIGN KEY (enhanced_casualty_severity) REFERENCES Enhanced_Casualty_Severity(enhanced_casualty_severity),
    FOREIGN KEY (casualty_distance_banding) REFERENCES Distance_Banding(distance_band_id)
);

CREATE TABLE Vehicle (
    vehicle_reference INTEGER PRIMARY KEY
);

CREATE TABLE Casualties_In_Collision (
    casualties_in_collision_id INTEGER PRIMARY KEY,
    casualty_reference INTEGER,
    vehicle_reference INTEGER,
    FOREIGN KEY (casualty_reference) REFERENCES Casualty(casualty_reference),
    FOREIGN KEY (vehicle_reference) REFERENCES Vehicle(vehicle_reference)
);

CREATE TABLE Collision (
    collision_year INTEGER,
    collision_ref_no INTEGER,
    casualties_in_collision_id INTEGER,
    PRIMARY KEY (collision_year, collision_ref_no),
    FOREIGN KEY (casualties_in_collision_id) REFERENCES Casualties_In_Collision(casualties_in_collision_id)
);
