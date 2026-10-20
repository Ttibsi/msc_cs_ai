import sqlite3
from typing import Final
from typing import Optional

# I was going to write my own contextmanager for sqlite, but turns out
# that this is the archetypical example.
# source: https://oneuptime.com/blog/post/2026-01-30-python-custom-context-managers/view
class DatabaseConnection:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # Handle transaction based on whether an exception occurred
        if exc_type is not None:
            self.connection.rollback()
            print(f"Transaction rolled back due to: {exc_val}")
        else:
            self.connection.commit()

        self.cursor.close()
        self.connection.close()
        return False


def main() -> None:
    # Step 1: create the database and tables
    create_table_cmds: Final[list[str]] = [
        "CREATE TABLE Collision (collision_index INTEGER PRIMARY KEY, collision_year INTEGER, collision_ref_no TEXT);",
        "CREATE TABLE Vehicle_Type (vehicle_type INTEGER PRIMARY KEY, vehicle_type_name TEXT);",
        "CREATE TABLE Vehicle (collision_index INTEGER, vehicle_reference INTEGER, vehicle_type INTEGER, PRIMARY KEY (collision_index, vehicle_reference), FOREIGN KEY (collision_index) REFERENCES Collision(collision_index), FOREIGN KEY (vehicle_type) REFERENCES Vehicle_Type(vehicle_type));",
        "CREATE TABLE Age_Band (age_band_id INTEGER PRIMARY KEY, age_band TEXT);",
        "CREATE TABLE Age_Band_to_Age (age INTEGER PRIMARY KEY, age_band_id INTEGER, FOREIGN KEY (age_band_id) REFERENCES Age_Band(age_band_id));",
        "CREATE TABLE Pedestrian_Location (pedestrian_location INTEGER PRIMARY KEY, description TEXT);",
        "CREATE TABLE Pedestrian_Movement (pedestrian_movement INTEGER PRIMARY KEY, description TEXT);",
        "CREATE TABLE Passenger_location (car_passenger INTEGER PRIMARY KEY, description TEXT);",
        "CREATE TABLE Bus_Coach_location (bus_or_coach_passenger INTEGER PRIMARY KEY, description TEXT);",
        "CREATE TABLE Maintenance_Worker (pedestrian_road_maintenance_worker INTEGER PRIMARY KEY, description TEXT);",
        "CREATE TABLE Casualty_Type (casualty_type_id INTEGER PRIMARY KEY, description TEXT);",
        "CREATE TABLE Casualty_Severity (casualty_severity_id INTEGER PRIMARY KEY, description TEXT);",
        "CREATE TABLE Casualty_Class (casualty_class TEXT PRIMARY KEY, description TEXT);",
        "CREATE TABLE Decile_type (casualty_imd_decile INTEGER PRIMARY KEY, description TEXT);",
        "CREATE TABLE Distance_Banding (distance_band_id INTEGER PRIMARY KEY, description TEXT);",
        "CREATE TABLE LSOA (lsoa_of_casualty TEXT PRIMARY KEY, casualty_imd_decile INTEGER, FOREIGN KEY (casualty_imd_decile) REFERENCES Decile_type(casualty_imd_decile));",
        "CREATE TABLE Casualty (collision_index INTEGER, casualty_reference INTEGER, casualty_class TEXT, sex_of_casualty TEXT, age_of_casualty INTEGER, enhanced_casualty_severity TEXT, pedestrian_location INTEGER, pedestrian_movement INTEGER, car_passenger INTEGER, bus_or_coach_passenger INTEGER, pedestrian_road_maintenance_worker INTEGER, casualty_type INTEGER, casualty_imd_decile INTEGER, lsoa_of_casualty TEXT, casualty_injury_based TEXT, casualty_adjusted_severity_serious TEXT, casualty_adjusted_severity_slight TEXT, distance_band_id INTEGER, casualty_severity INTEGER, vehicle_reference INTEGER, PRIMARY KEY (collision_index, casualty_reference), FOREIGN KEY (collision_index) REFERENCES Collision(collision_index), FOREIGN KEY (casualty_class) REFERENCES Casualty_Class(casualty_class), FOREIGN KEY (age_of_casualty) REFERENCES Age_Band_to_Age(age), FOREIGN KEY (pedestrian_location) REFERENCES Pedestrian_Location(pedestrian_location), FOREIGN KEY (pedestrian_movement) REFERENCES Pedestrian_Movement(pedestrian_movement), FOREIGN KEY (car_passenger) REFERENCES Passenger_location(car_passenger), FOREIGN KEY (bus_or_coach_passenger) REFERENCES Bus_Coach_location(bus_or_coach_passenger), FOREIGN KEY (pedestrian_road_maintenance_worker) REFERENCES Maintenance_Worker(pedestrian_road_maintenance_worker), FOREIGN KEY (casualty_type) REFERENCES Casualty_Type(casualty_type_id), FOREIGN KEY (casualty_imd_decile) REFERENCES Decile_type(casualty_imd_decile), FOREIGN KEY (lsoa_of_casualty) REFERENCES LSOA(lsoa_of_casualty), FOREIGN KEY (distance_band_id) REFERENCES Distance_Banding(distance_band_id), FOREIGN KEY (casualty_severity) REFERENCES Casualty_Severity(casualty_severity_id), FOREIGN KEY (collision_index, vehicle_reference) REFERENCES Vehicle(collision_index, vehicle_reference));"
    ]

    with DatabaseConnection("db.db") as cur:
        for cmd in create_table_cmds:
            cur.execute(cmd)

    # Step 2: insert data from csv file
    with DatabaseConnection("db.db") as cur:
        with open("dft-road-casualty-statistics-casualty-2024.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                ...

    # Step 3: extract all casualties who:
        # - suffered serious or fatal injuries
        # - were involved in pedestrian-related incidents
        # - occured under a specific condition
            # NOTE: I think the last one is up to us to decide
    query_cmds: Final[list[str]] = [
    ]

    with DatabaseConnection("db.db") as cur:
        for cmd in query_cmds:
            res = cur.execute(cmd)
            res.fetchone()

    # Step 4: Perform descriptive analysis of casualty severity by casualty type
    # (aggregation query)


if __name__ == "__main__":
    raise SystemExit(main())
