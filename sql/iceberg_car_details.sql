-- Iceberg table for car detail fact data
-- Creates car_detail table in Iceberg with UPSERT support using MERGE INTO
-- Supports both local SQLite catalog and AWS Glue catalog

CREATE TABLE IF NOT EXISTS car_detail (
    car_id VARCHAR NOT NULL,
    engine_type VARCHAR,
    displacement VARCHAR,
    horsepower INT,
    top_speed INT,
    zero_to_sixty VARCHAR,
    length VARCHAR,
    weight VARCHAR,
    fuel_economy VARCHAR,
    safety_features TEXT
)
USING ICEBERG;

-- Create primary key constraint using car_id
ALTER TABLE car_detail ADD CONSTRAINT pk_car_detail PRIMARY KEY (car_id);

-- For UPSERT operations in Iceberg, use MERGE INTO with PyArrow/Spark:
-- MERGE INTO car_detail t
-- USING new_car_details s
-- ON t.car_id = s.car_id
-- WHEN MATCHED THEN UPDATE SET *
-- WHEN NOT MATCHED THEN INSERT *;