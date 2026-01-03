CREATE TABLE IF NOT EXISTS car_details (
    car_id VARCHAR PRIMARY KEY,
    engine_type VARCHAR,
    displacement VARCHAR,
    horsepower INT,
    top_speed INT,
    zero_to_sixty VARCHAR,
    length VARCHAR,
    weight VARCHAR,
    fuel_economy VARCHAR,
    safety_features TEXT
);
