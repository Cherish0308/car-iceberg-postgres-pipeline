CREATE TABLE IF NOT EXISTS cars (
    car_id VARCHAR PRIMARY KEY,
    brand_name VARCHAR,
    country VARCHAR,
    model_name VARCHAR,
    model_year INT
);

CREATE TABLE IF NOT EXISTS car_detail (
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