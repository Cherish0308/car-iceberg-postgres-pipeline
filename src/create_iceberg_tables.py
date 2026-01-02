from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import StringType, IntegerType, NestedField
from config import ICEBERG_WAREHOUSE
import os

# Ensure warehouse directory exists
os.makedirs(ICEBERG_WAREHOUSE, exist_ok=True)

catalog = load_catalog(
    "local",
    **{
        "type": "sql",
        "uri": f"sqlite:///{ICEBERG_WAREHOUSE}/catalog.db",
        "warehouse": f"file://{ICEBERG_WAREHOUSE}"
    }
)

# Create namespace if it doesn't exist
try:
    catalog.create_namespace("default")
    print("✓ Created namespace: default")
except Exception as e:
    print(f"Namespace exists or error: {e}")

# Create cars table
try:
    cars_schema = Schema(
        NestedField(1, "car_id", StringType(), required=True),
        NestedField(2, "brand_name", StringType(), required=False),
        NestedField(3, "country", StringType(), required=False),
        NestedField(4, "model_name", StringType(), required=False),
        NestedField(5, "model_year", IntegerType(), required=False),
    )
    
    catalog.create_table(
        identifier="default.cars",
        schema=cars_schema
    )
    print("✓ Created cars table")
except Exception as e:
    print(f"Cars table exists or error: {e}")

# Create car_detail table
try:
    car_detail_schema = Schema(
        NestedField(1, "car_id", StringType(), required=True),
        NestedField(2, "engine_type", StringType(), required=False),
        NestedField(3, "displacement", StringType(), required=False),
        NestedField(4, "horsepower", IntegerType(), required=False),
        NestedField(5, "top_speed", IntegerType(), required=False),  # Changed to Integer to match data
        NestedField(6, "zero_to_sixty", StringType(), required=False),
        NestedField(7, "length", StringType(), required=False),
        NestedField(8, "weight", StringType(), required=False),
        NestedField(9, "fuel_economy", StringType(), required=False),
        NestedField(10, "safety_features", StringType(), required=False),
    )
    
    catalog.create_table(
        identifier="default.car_detail",
        schema=car_detail_schema
    )
    print("✓ Created car_detail table")
except Exception as e:
    print(f"Car_detail table exists or error: {e}")

print("\nIceberg tables created successfully!")
