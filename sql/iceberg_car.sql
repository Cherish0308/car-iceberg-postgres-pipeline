-- Iceberg table for car dimension data
-- Creates cars table in Iceberg with UPSERT support using MERGE INTO
-- Supports both local SQLite catalog and AWS Glue catalog

CREATE TABLE IF NOT EXISTS cars (
    car_id VARCHAR NOT NULL,
    brand_name VARCHAR,
    country VARCHAR,
    model_name VARCHAR,
    model_year INT
)
USING ICEBERG
PARTITIONED BY (model_year);

-- Create primary key constraint using car_id
ALTER TABLE cars ADD CONSTRAINT pk_cars PRIMARY KEY (car_id);

-- For UPSERT operations in Iceberg, use MERGE INTO with PyArrow/Spark:
-- MERGE INTO cars t
-- USING new_cars s
-- ON t.car_id = s.car_id
-- WHEN MATCHED THEN UPDATE SET *
-- WHEN NOT MATCHED THEN INSERT *;