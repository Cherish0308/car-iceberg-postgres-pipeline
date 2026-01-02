"""
IcebergWriter implementation following SRP, OCP, LSP, and DIP.
SRP: Only responsible for Iceberg table operations.
OCP: Writer protocol allows new storage backends without modifying this class.
LSP: Can substitute any Writer implementation.
DIP: Depends on PyIceberg catalog abstraction, can be injected.
"""
from __future__ import annotations

from pyiceberg.catalog import load_catalog
from config import ICEBERG_WAREHOUSE
import os


class IcebergWriter:
    """
    Writes data to Iceberg tables with upsert support.
    Following SRP: Single responsibility of Iceberg persistence.
    
    Note: PyIceberg append-only. For true UPSERT in production, use Spark with MERGE INTO.
    """

    def __init__(self, catalog=None):
        """
        Initialize Iceberg writer.
        
        Args:
            catalog: PyIceberg catalog (injectable for testing).
        """
        if catalog is None:
            os.makedirs(ICEBERG_WAREHOUSE, exist_ok=True)
            catalog = load_catalog(
                "local",
                **{
                    "type": "sql",
                    "uri": f"sqlite:///{ICEBERG_WAREHOUSE}/catalog.db",
                    "warehouse": f"file://{ICEBERG_WAREHOUSE}"
                }
            )
        self._catalog = catalog

    def upsert(self, table_name: str, records: list[dict]) -> None:
        """
        Upsert records into Iceberg table using delete + append pattern.
        
        UPSERT Strategy:
        1. Delete existing records with matching car_ids
        2. Append new records
        
        Args:
            table_name: Table name to upsert into.
            records: List of records as dictionaries.
        """
        if not records:
            return
        
        try:
            import pyarrow as pa
            
            table = self._catalog.load_table(f"default.{table_name}")
            
            # Create explicit PyArrow schema matching Iceberg
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
            
            # New data
            new_df = pa.Table.from_pylist(records, schema=schema)
            new_car_ids = [records[r]['car_id'] for r in range(len(records))]
            
            # Delete existing records with matching car_ids (UPSERT: delete old)
            try:
                from pyiceberg.expressions import In
                table.delete(In("car_id", new_car_ids))
            except Exception:
                # Table might be empty on first run
                pass
            
            # Append new records (UPSERT: insert new/updated)
            table.append(new_df)
            
        except Exception as e:
            # Log but don't fail the entire pipeline
            print(f"Warning: Iceberg write failed for {table_name}: {e}")

