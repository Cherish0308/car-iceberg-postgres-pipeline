from __future__ import annotations

from pyiceberg.catalog import load_catalog
from config import ICEBERG_WAREHOUSE, GLUE_ENABLED, GLUE_CATALOG_NAME, AWS_REGION
import os
import tempfile


class IcebergWriter:

    def __init__(self, catalog=None):
        if catalog is None:
            if GLUE_ENABLED:
                print(f"Loading AWS Glue Catalog: {GLUE_CATALOG_NAME}")
                print(f"Iceberg warehouse: {ICEBERG_WAREHOUSE}")
                catalog = load_catalog(
                    GLUE_CATALOG_NAME,
                    **{
                        "type": "glue",
                        "s3.region": AWS_REGION,
                    }
                )
            else:
                catalog_path = os.path.join(tempfile.gettempdir(), "iceberg_catalog.db")
                print(f"Loading SQLite Catalog with S3 storage")
                print(f"Catalog DB: {catalog_path}")
                print(f"Iceberg warehouse (S3): {ICEBERG_WAREHOUSE}")
                
                catalog = load_catalog(
                    "default",
                    **{
                        "type": "sql",
                        "uri": f"sqlite:///{catalog_path}",
                        "warehouse": ICEBERG_WAREHOUSE,
                        "s3.region": AWS_REGION,
                    }
                )
        self._catalog = catalog

    def upsert(self, table_name: str, records: list[dict]) -> None:
        if not records:
            return
        
        try:
            import pyarrow as pa
            
            table = self._catalog.load_table(f"default.{table_name}")
            
            if table_name == "cars":
                schema = pa.schema([
                    pa.field("car_id", pa.string(), nullable=False),
                    pa.field("brand_name", pa.string(), nullable=True),
                    pa.field("country", pa.string(), nullable=True),
                    pa.field("model_name", pa.string(), nullable=True),
                    pa.field("model_year", pa.int32(), nullable=True),
                ])
            elif table_name == "car_detail":
                schema = pa.schema([
                    pa.field("car_id", pa.string(), nullable=False),
                    pa.field("engine_type", pa.string(), nullable=True),
                    pa.field("displacement", pa.string(), nullable=True),
                    pa.field("horsepower", pa.int32(), nullable=True),
                    pa.field("top_speed", pa.int32(), nullable=True),
                    pa.field("zero_to_sixty", pa.string(), nullable=True),
                    pa.field("length", pa.string(), nullable=True),
                    pa.field("weight", pa.string(), nullable=True),
                    pa.field("fuel_economy", pa.string(), nullable=True),
                    pa.field("safety_features", pa.string(), nullable=True),
                ])
            else:
                raise ValueError(f"Unknown table: {table_name}")
            
            new_df = pa.Table.from_pylist(records, schema=schema)
            new_car_ids = [record['car_id'] for record in records]
            
            from pyiceberg.expressions import In
            try:
                delete_filter = In("car_id", new_car_ids)
                table.delete(delete_filter)
                print(f"  Deleted existing records for {len(new_car_ids)} car_ids from {table_name}")
            except Exception as del_err:
                print(f"  Delete operation skipped for {table_name}: {del_err}")
            
            table.append(new_df)
            print(f"  Appended {len(records)} records to {table_name}")
            
        except Exception as e:
            print(f"Warning: Iceberg write failed for {table_name}: {e}")
            print(f"Warning: Iceberg write failed for {table_name}: {e}")

